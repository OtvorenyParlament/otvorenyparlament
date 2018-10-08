"""
Parliament GraphQL Types and Queries
"""

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphql_utils import CountableConnectionBase, OrderedDjangoFilterConnectionField
from parliament.models import (
    Club,
    Member,
    Period,
    Press,
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


class ParliamentQueries(graphene.ObjectType):

    club = graphene.relay.Node.Field(ClubType)
    all_clubs = DjangoFilterConnectionField(ClubType)

    period = graphene.relay.Node.Field(PeriodType)
    all_periods = DjangoFilterConnectionField(PeriodType)

    press = graphene.relay.Node.Field(PressType)
    all_presses = DjangoFilterConnectionField(PressType)

    member = graphene.relay.Node.Field(MemberType)
    all_members = OrderedDjangoFilterConnectionField(
        MemberType, orderBy=graphene.List(of_type=graphene.String))
