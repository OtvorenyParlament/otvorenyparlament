"""
Parliament GraphQL Types and Queries
"""

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from parliament.models import Club, Period


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


class ParliamentQueries(graphene.ObjectType):

    club = graphene.relay.Node.Field(ClubType)
    all_clubs = DjangoFilterConnectionField(ClubType)

    period = graphene.relay.Node.Field(PeriodType)
    all_periods = DjangoFilterConnectionField(PeriodType)
