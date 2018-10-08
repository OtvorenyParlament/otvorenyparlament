"""
Parliament GraphQL Types and Queries
"""

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphql_utils import CountableConnectionBase, OrderedDjangoFilterConnectionField
from parliament.filters import VotingVoteFilterSet
from parliament.models import (
    Club,
    ClubMember,
    Member,
    Period,
    Press,
    # PressAttachment,
    Session,
    SessionProgram,
    # SessionAttachment,
    Voting,
    VotingVote,
)


class ClubType(DjangoObjectType):

    class Meta:
        model = Club
        description = 'Club'
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'id': ('exact',),
            'period__period_num': ('exact',)
        }
        only_fields = ['name', 'external_id', 'period']


class ClubMemberType(DjangoObjectType):

    class Meta:
        model = ClubMember
        description = 'Club Member'
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'id': ('exact',),
            'club': ('exact',)
        }
        only_fields = ['club', 'member', 'membership', 'start', 'end']


class PeriodType(DjangoObjectType):

    class Meta:
        model = Period
        description = 'Period'
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'id': ('exact',),
            'period_num': ('exact',)
        }
        only_fields = ['id', 'period_num', 'year_start', 'year_end', 'snap_end']


class PressType(DjangoObjectType):
    class Meta:
        model = Press
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'id': ('exact',),
            'press_num': ('exact',),
            'press_type': ('exact',),
            'period__period_num': ('exact',)
        }


class MemberType(DjangoObjectType):

    class Meta:
        interfaces = (graphene.relay.Node,)
        model = Member
        filter_fields = {
            'id': ('exact',),
            'stood_for_party': ('exact',),
            'period__period_num': ('exact',)
        }
        connection_class = CountableConnectionBase


class SessionType(DjangoObjectType):
    class Meta:
        model = Session
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            'id': ('exact',),
            'session_num': ('exact',),
            'period__period_num': ('exact',)
        }
        connection_class = CountableConnectionBase


class SessionProgramPointType(DjangoObjectType):
    class Meta:
        model = SessionProgram
        interfaces = (graphene.relay.Node,)
        connection_class = CountableConnectionBase
        filter_fields = {
            'id': ('exact',)
        }


class VotingChartSeriesType(graphene.ObjectType):
    labels = graphene.List(graphene.String)
    series = graphene.List(graphene.Int)


class VotingType(DjangoObjectType):

    chart_series = graphene.Field(VotingChartSeriesType)

    class Meta:
        model = Voting
        connection_class = CountableConnectionBase
        interfaces = (graphene.relay.Node, )
        filter_fields = {
            'id': ('exact',),
            'session__session_num': ('exact',),
            'session__period__period_num': ('exact',)
        }

    @classmethod
    def get_node(cls, info, id):
        node = Voting.objects.get(id=id)
        return node

    @classmethod
    def get_connection(cls):
        class CountableConnection(graphene.relay.Connection):
            total_count = graphene.Int()

            class Meta:
                name = '{}Connection'.format(cls._meta.name)
                node = cls

            @staticmethod  # Redundant since Graphene kinda does this automatically for all resolve_ methods.
            def resolve_total_count(root, args, context, info):
                return root.length

        return CountableConnection

    def resolve_chart_series(self, info):
        return VotingChartSeriesType(**self.chart_series())


class VotingVoteType(DjangoObjectType):

    class Meta:
        model = VotingVote
        interfaces = (graphene.relay.Node, )
        connection_class = CountableConnectionBase

    @classmethod
    def get_node(cls, info, id):
        node = VotingVote.objects.get(id=id)
        return node

    @classmethod
    def get_connection(cls):
        class CountableConnection(graphene.relay.Connection):
            total_count = graphene.Int()

            class Meta:
                name = '{}Connection'.format(cls._meta.name)
                node = cls

            @staticmethod  # Redundant since Graphene kinda does this automatically for all resolve_ methods.
            def resolve_total_count(root, args, context, info):
                return root.length

        return CountableConnection


class ParliamentQueries(graphene.ObjectType):

    club = graphene.relay.Node.Field(ClubType)
    all_clubs = DjangoFilterConnectionField(ClubType)

    club_member = graphene.relay.Node.Field(ClubMemberType)
    all_club_members = DjangoFilterConnectionField(ClubMemberType)

    period = graphene.relay.Node.Field(PeriodType)
    all_periods = DjangoFilterConnectionField(PeriodType)

    press = graphene.relay.Node.Field(PressType)
    all_presses = DjangoFilterConnectionField(PressType)

    session = graphene.relay.Node.Field(SessionType)
    all_sessions = OrderedDjangoFilterConnectionField(
        SessionType, orderBy=graphene.List(of_type=graphene.String))

    session_program_point = graphene.relay.Node.Field(SessionProgramPointType)
    all_session_program_points = OrderedDjangoFilterConnectionField(
        SessionProgramPointType, orderBy=graphene.List(of_type=graphene.String))

    voting = graphene.relay.Node.Field(VotingType)
    all_votings = OrderedDjangoFilterConnectionField(
        VotingType, orderBy=graphene.List(of_type=graphene.String))

    voting_vote = graphene.relay.Node.Field(VotingVoteType)
    all_voting_votes = OrderedDjangoFilterConnectionField(
        VotingVoteType,
        orderBy=graphene.List(of_type=graphene.String),
        filterset_class=VotingVoteFilterSet)

    member = graphene.relay.Node.Field(MemberType)
    all_members = OrderedDjangoFilterConnectionField(
        MemberType, orderBy=graphene.List(of_type=graphene.String))
