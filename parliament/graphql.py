"""
Parliament GraphQL Types and Queries
"""

import graphene
from graphene.relay import Node
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphql_utils import CountableConnectionBase, OrderedDjangoFilterConnectionField
from parliament.filters import (
    AmendmentFilterSet,
    BillFilterSet,
    ClubMemberFilterSet,
    CommitteeMemberFilterSet,
    MemberFilterSet,
    VotingVoteFilterSet
)
from parliament.models import (
    Amendment,
    AmendmentSignedMember,
    AmendmentSubmitter,
    Bill,
    BillProcessStep,
    BillProposer,
    Club,
    ClubMember,
    Committee,
    CommitteeMember,
    CommitteeSession,
    CommitteeSessionPoint,
    DebateAppearance,
    Interpellation,
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


# TODO(Jozef): Add overridden DjangoObjectType implicitly containing
# interfaces = (Node,) and CountableConnectionBase as connection_class

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
        only_fields = ['club', 'member', 'membership', 'start', 'end']
        connection_class = CountableConnectionBase


class ClubType(DjangoObjectType):

    current_member_count = graphene.Int()

    class Meta:
        model = Club
        description = 'Club'
        interfaces = (Node,)
        filter_fields = {
            'id': ('exact',),
            'period__period_num': ('exact',)
        }
        only_fields = ['name', 'period', 'members', 'current_member_count', 'coalition']


class CommitteeMemberType(DjangoObjectType):

    class Meta:
        model = CommitteeMember
        description = 'Committee Member'
        interfaces = (Node,)
        only_fields = ['committee', 'member', 'membership', 'start', 'end']
        connection_class = CountableConnectionBase


class CommitteeType(DjangoObjectType):

    class Meta:
        model = Committee
        description = 'Committee'
        interfaces = (Node,)
        filter_fields = {
            'id': ('exact',),
            'period__period_num': ('exact',)
        }
        only_fields = ['name', 'period', 'members', 'description']
        connection_class = CountableConnectionBase


class CommitteeSessionPointType(DjangoObjectType):

    class Meta:
        model = CommitteeSessionPoint
        description = 'Committee Session Point'
        interfaces = (Node,)
        filter_fields = {
            'id': ('exact',),
            'session': ('exact',)
        }
        only_fields = ['session', 'index', 'topic', 'press']
        connection_class = CountableConnectionBase


class CommitteeSessionType(DjangoObjectType):

    class Meta:
        model = CommitteeSession
        description = 'Committee Session'
        interfaces = (Node,)
        filter_fields = {
            'id': ('exact',),
            'committee': ('exact',),
        }
        only_fields = ['committee', 'start', 'end', 'place', 'points']
        connection_class = CountableConnectionBase


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


class DebateAppearanceType(DjangoObjectType):

    class Meta:
        interfaces = (Node,)
        model = DebateAppearance
        connection_class = CountableConnectionBase
        filter_fields = {
            'id': ('exact',),
            'debater': ('exact',),
        }


class InterpellationType(DjangoObjectType):

    status_display = graphene.String()

    class Meta:
        interfaces = (Node,)
        model = Interpellation
        connection_class = CountableConnectionBase
        filter_fields = {
            'id': ('exact',),
            'asked_by': ('exact',),
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
    result_display = graphene.String()

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


class BillProposerType(DjangoObjectType):

    class Meta:
        model = BillProposer
        interfaces = (Node,)
        connection_class = CountableConnectionBase
        filter_fields = {
            'member': ('exact',),
            'bill': ('exact',)
        }


class BillType(DjangoObjectType):

    class Meta:
        model = Bill
        interfaces = (Node,)
        connection_class = CountableConnectionBase
        only_fields = [
            'external_id', 'category', 'press', 'delivered',
            'proposer_nonmember', 'proposers', 'state', 'result', 'url'
        ]


class BillProcessStepType(DjangoObjectType):

    class Meta:
        model = BillProcessStep
        interfaces = (Node,)
        connection_class = CountableConnectionBase
        filter_fields = {
            'id': ('exact',)
        }


class AmendmentSignedMemberType(DjangoObjectType):

    class Meta:
        model = AmendmentSignedMember
        interfaces = (Node,)
        connection_class = CountableConnectionBase
        filter_fields = {
            'id': ('exact',)
        }


class AmendmentSubmitterType(DjangoObjectType):

    class Meta:
        model = AmendmentSubmitter
        interfaces = (Node,)
        connection_class = CountableConnectionBase
        filter_fields = {
            'id': ('exact',)
        }


class AmendmentType(DjangoObjectType):

    class Meta:
        model = Amendment
        interfaces = (Node,)
        connection_class = CountableConnectionBase


class ParliamentQueries(graphene.ObjectType):

    club_member = Node.Field(ClubMemberType)
    all_club_members = OrderedDjangoFilterConnectionField(
        ClubMemberType,
        orderBy=graphene.List(of_type=graphene.String),
        filterset_class=ClubMemberFilterSet
    )

    club = Node.Field(ClubType)
    all_clubs = OrderedDjangoFilterConnectionField(
        ClubType, orderBy=graphene.List(of_type=graphene.String))

    committee_member = Node.Field(CommitteeMemberType)
    all_committee_members = OrderedDjangoFilterConnectionField(
        CommitteeMemberType,
        orderBy=graphene.List(of_type=graphene.String),
        filterset_class=CommitteeMemberFilterSet
    )

    committee = Node.Field(CommitteeType)
    all_committees = OrderedDjangoFilterConnectionField(
        CommitteeType,
        orderBy=graphene.List(of_type=graphene.String),
    )

    committee_session = Node.Field(CommitteeSessionType)
    all_committee_sessions = OrderedDjangoFilterConnectionField(
        CommitteeSessionType,
        orderBy=graphene.List(of_type=graphene.String),
    )

    committee_session_point = Node.Field(CommitteeSessionPointType)
    all_committee_session_points = OrderedDjangoFilterConnectionField(
        CommitteeSessionPointType,
        orderBy=graphene.List(of_type=graphene.String),
    )

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

    debate_appearance = Node.Field(DebateAppearanceType)
    all_debate_appearances = OrderedDjangoFilterConnectionField(
        DebateAppearanceType,
        orderBy=graphene.List(of_type=graphene.String),
        club=graphene.ID()
    )

    interpellation = Node.Field(InterpellationType)
    all_interpellations = OrderedDjangoFilterConnectionField(
        InterpellationType,
        orderBy=graphene.List(of_type=graphene.String),
        club=graphene.ID()
    )

    member = Node.Field(MemberType)
    all_members = OrderedDjangoFilterConnectionField(
        MemberType,
        orderBy=graphene.List(of_type=graphene.String),
        filterset_class=MemberFilterSet,
    )

    bill = Node.Field(BillType)
    all_bills = OrderedDjangoFilterConnectionField(
        BillType,
        orderBy=graphene.List(of_type=graphene.String),
        filterset_class=BillFilterSet
    )

    bill_proposer = Node.Field(BillProposerType)
    all_bill_proposers = OrderedDjangoFilterConnectionField(
        BillProposerType,
        orderBy=graphene.List(of_type=graphene.String),
    )

    bill_process_step = Node.Field(BillProcessStepType)
    all_bill_process_steps = OrderedDjangoFilterConnectionField(
        BillProcessStepType,
        orderBy=graphene.List(of_type=graphene.String),
    )

    amendment = Node.Field(AmendmentType)
    all_amendments = OrderedDjangoFilterConnectionField(
        AmendmentType,
        orderBy=graphene.List(of_type=graphene.String),
        filterset_class=AmendmentFilterSet,
        club=graphene.ID()
    )
