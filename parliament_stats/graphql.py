"""
Graphene Stats
"""

from django.db.models import Sum

import graphene
from graphene import ObjectType
from graphene.utils.str_converters import to_snake_case
from graphql_relay.node.node import from_global_id

from parliament.models import Club
from parliament_stats.models import ClubStats
from parliament_stats.types import ColumnClubStatsType


class ClubStatsType(ColumnClubStatsType):

    class Meta:
        model = ClubStats
        exclude_fields = ['id', 'date']


class ParliamentStatsQueries(ObjectType):

    club_stats = graphene.Field(ClubStatsType, club=graphene.ID(required=True))

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
            if x.name.value not in ['club', 'date']
        ]

        sums = {x: Sum(x) for x in fields_to_aggregate}

        club_stats = list(club.club_stats.all().values('club').annotate(**sums))[0]
        club_stats['club'] = club
        return ClubStatsType(**club_stats)
