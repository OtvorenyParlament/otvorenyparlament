"""
Parliament GraphQL Types
"""

import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from parliament.models import Period


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

    period = graphene.relay.Node.Field(PeriodType)
    all_periods = DjangoFilterConnectionField(PeriodType)
