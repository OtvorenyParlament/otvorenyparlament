"""
Person GraphQL Types and Queries
"""

import graphene
from graphene_django import DjangoObjectType

from graphql_utils import CountableConnectionBase, OrderedDjangoFilterConnectionField
from person.models import Person


class PersonType(DjangoObjectType):
    """
    Parliament Person type
    """
    full_name = graphene.String()

    class Meta:
        interfaces = (graphene.relay.Node,)
        model = Person
        filter_fields = {
            'id': ('exact',),
            'forename': ('icontains',),
            'surname': ('icontains',),
            'memberships__period__period_num': ('exact',)
        }
        connection_class = CountableConnectionBase


class PersonQueries(graphene.ObjectType):

    person = graphene.relay.Node.Field(PersonType)
    all_persons = OrderedDjangoFilterConnectionField(PersonType)
