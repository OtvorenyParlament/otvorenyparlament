"""
Parliament GraphQL Types and Queries
"""

import graphene
from graphene.relay import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphql_utils import CountableConnectionBase, OrderedDjangoFilterConnectionField
from parliament.filters import MemberFilterSet, VotingVoteFilterSet
from parliament.models import (
    Club,
    ClubMember,
    Member,
    MemberActive,
    Party,
    Period,
    Press,
    # PressAttachment,
    Session,
    SessionProgram,
    # SessionAttachment,
    Voting,
    VotingVote,
)


class PartyType(DjangoObjectType):

    class Meta:
        model = Party
        description = 'Stood For Party'
        interfaces = (Node,)


class ClubMemberType(DjangoObjectType):

    class Meta:
        model = ClubMember
        description = 'Club Member'
        interfaces = (Node,)
        filter_fields = {
            'id': ('exact',),
            'club': ('exact',)
        }
        only_fields = ['club', 'member', 'membership', 'start', 'end']


class ClubType(DjangoObjectType):

    class Meta:
        model = Club
        description = 'Club'
        interfaces = (Node,)
        filter_fields = {
            'id': ('exact',),
            'period__period_num': ('exact',)
        }
        only_fields = ['name', 'period', 'members']


class PeriodType(DjangoObjectType):

    class Meta:
        model = Period
        description = 'Period'
        interfaces = (Node,)
        filter_fields = {
            'id': ('exact',),
            'period_num': ('exact',)
        }
        only_fields = ['id', 'period_num', 'start_date', 'end_date', 'snap_end']


class PressType(DjangoObjectType):
    class Meta:
        model = Press
        interfaces = (Node,)
        filter_fields = {
            'id': ('exact',),
            'press_num': ('exact',),
            'press_type': ('exact',),
            'period__period_num': ('exact',)
        }


class MemberType(DjangoObjectType):

    class Meta:
        interfaces = (Node,)
        model = Member
        connection_class = CountableConnectionBase


class MemberActiveType(DjangoObjectType):

    class Meta:
        interfaces = (Node,)
        model = MemberActive
        connection_class = CountableConnectionBase


class SessionType(DjangoObjectType):
    class Meta:
        model = Session
        interfaces = (Node,)
        filter_fields = {
            'id': ('exact',),
            'session_num': ('exact',),
            'period__period_num': ('exact',)
        }
        connection_class = CountableConnectionBase


class SessionProgramPointType(DjangoObjectType):
    class Meta:
        model = SessionProgram
        interfaces = (Node,)
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
        interfaces = (Node, )
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
        interfaces = (Node, )
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

    club_member = Node.Field(ClubMemberType)
    all_club_members = DjangoFilterConnectionField(ClubMemberType)

    club = Node.Field(ClubType)
    all_clubs = DjangoFilterConnectionField(ClubType)

    period = Node.Field(PeriodType)
    all_periods = DjangoFilterConnectionField(PeriodType)

    press = Node.Field(PressType)
    all_presses = DjangoFilterConnectionField(PressType)

    session = Node.Field(SessionType)
    all_sessions = OrderedDjangoFilterConnectionField(
        SessionType, orderBy=graphene.List(of_type=graphene.String))

    session_program_point = Node.Field(SessionProgramPointType)
    all_session_program_points = OrderedDjangoFilterConnectionField(
        SessionProgramPointType, orderBy=graphene.List(of_type=graphene.String))

    voting = Node.Field(VotingType)
    all_votings = OrderedDjangoFilterConnectionField(
        VotingType, orderBy=graphene.List(of_type=graphene.String))

    voting_vote = Node.Field(VotingVoteType)
    all_voting_votes = OrderedDjangoFilterConnectionField(
        VotingVoteType,
        orderBy=graphene.List(of_type=graphene.String),
        filterset_class=VotingVoteFilterSet)

    member = Node.Field(MemberType)
    all_members = OrderedDjangoFilterConnectionField(
        MemberType,
        orderBy=graphene.List(of_type=graphene.String),
        filterset_class=MemberFilterSet,
    )
