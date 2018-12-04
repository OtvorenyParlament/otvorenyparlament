"""
Graphene Stats
"""

from django.db.models import F, Sum

import graphene
from graphene import ObjectType
from graphene.utils.str_converters import to_snake_case
from graphql_relay.node.node import from_global_id

from parliament.graphql import ClubType
from parliament.models import Club, Member, Period
from parliament_stats.models import ClubStats, GlobalStats, MemberStats
from parliament_stats.types import ColumnStatsType


class ClubStatsType(ColumnStatsType):

    class Meta:
        model = ClubStats
        exclude_fields = ['id', 'date']
        # TODO(Jozef): check TODO in types.py
        # group_fields = ['votingCoalition', 'votingOpposition']


class GlobalStatsType(ColumnStatsType):

    class Meta:
        model = GlobalStats
        exclude_fields = ['id', 'date']

class GlobalClubStatsType(ObjectType):

    club = graphene.Field(ClubType)
    bill_count = graphene.Int()
    amendment_count = graphene.Int()
    interpellation_count = graphene.Int()

    class Meta:
        interfaces = (graphene.relay.Node,)


class GlobalClubStatsConnection(graphene.Connection):

    total_count = graphene.Int()

    class Meta:
        node = GlobalClubStatsType


class MemberStatsType(ColumnStatsType):

    class Meta:
        model = MemberStats
        exclude_fields = ['id', 'date']


class ParliamentStatsQueries(ObjectType):

    club_stats = graphene.Field(ClubStatsType, club=graphene.ID(required=True))
    global_stats = graphene.Field(GlobalStatsType, period_num=graphene.Int(required=True))
    #global_club_stats = graphene.Field(graphene.List(GlobalClubStatsType))
    global_club_stats = graphene.relay.ConnectionField(
        GlobalClubStatsConnection, period_num=graphene.Int(required=True))
    member_stats = graphene.Field(MemberStatsType, member=graphene.ID(required=True))

    def resolve_club_stats(self, info, club):
        try:
            club_tuple = from_global_id(club)
            if not club_tuple:
                raise Exception()
            if not isinstance(club_tuple, tuple):
                raise Exception()
            if club_tuple[0] != 'ClubType':
                raise Exception()
        except:
            raise Exception("Malformed club ID")

        try:
            club = Club.objects.get(id=club_tuple[1])
        except Club.DoesNotExist:
            raise Exception("Requested club does not exist")

        fields_to_aggregate = [
            to_snake_case(x.name.value) for x in info.field_asts[0].selection_set.selections
            if x.name.value and x.name.value not in ['club', 'date', '__typename']
        ]

        sums = {x: Sum(x) for x in fields_to_aggregate}

        club_stats = list(club.club_stats.all().values('club').annotate(**sums))[0]
        club_stats['club'] = club
        return ClubStatsType(**club_stats)

    def resolve_global_stats(self, info, period_num):
        try:
            period = Period.objects.get(period_num=period_num)
        except Period.DoesNotExist:
            raise Exception("Requested period does not exist")
        fields_to_aggregate = [
            to_snake_case(x.name.value) for x in info.field_asts[0].selection_set.selections
            if x.name.value and x.name.value not in ['period', 'date', '__typename']
        ]

        sums = {x: Sum(x) for x in fields_to_aggregate}
        global_stats = list(period.global_stats.all().values('period').annotate(**sums))[0]
        global_stats['period'] = period
        return GlobalStatsType(**global_stats)

    def resolve_global_club_stats(self, info, period_num):

        try:
            period = Period.objects.get(period_num=period_num)
        except Period.DoesNotExist:
            raise Exception("Requested period does not exist")

        fields_to_aggregate = {}
        for field in info.field_asts[0].selection_set.selections[0].selection_set.selections[0].selection_set.selections:
            if field.name.value == 'billCount':
                fields_to_aggregate['bill_count'] = Sum('bill_count')
            if field.name.value == 'amendmentCount':
                fields_to_aggregate['amendment_count'] = Sum(
                    F('amendment_coalition') + F('amendment_opposition'))
            if field.name.value == 'interpellationCount':
                fields_to_aggregate['interpellation_count'] = Sum('interpellation_count')

        results = ClubStats.objects.filter(club__period=period).values('club').annotate(**fields_to_aggregate)

        clubs = {y.id: y for y in Club.objects.filter(id__in=[x['club'] for x in results])}
        for result in results:
            result['club'] = clubs[result['club']]

        return [GlobalClubStatsType(**x) for x in results]

    def resolve_member_stats(self, info, member):
        try:
            member_tuple = from_global_id(member)
            if not member_tuple:
                raise Exception()
            if not isinstance(member_tuple, tuple):
                raise Exception()
            if member_tuple[0] != 'MemberType':
                raise Exception()
        except:
            raise Exception("Malformed member ID")

        try:
            member = Member.objects.get(id=member_tuple[1])
        except Member.DoesNotExist:
            raise Exception("Requested member does not exist")

        fields_to_aggregate = [
            to_snake_case(x.name.value) for x in info.field_asts[0].selection_set.selections
            if x.name.value and x.name.value not in ['member', 'date', '__typename']
        ]

        sums = {x: Sum(x) for x in fields_to_aggregate}

        member_stats = list(member.member_stats.all().values('member').annotate(**sums))[0]
        member_stats['member'] = member
        return MemberStatsType(**member_stats)
