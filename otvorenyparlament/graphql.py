"""
GraphQL Schema
"""

import graphene

from geo.graphql import GeoQueries
from parliament.graphql import ParliamentQueries
from person.graphql import PersonQueries


class Queries(GeoQueries, ParliamentQueries, PersonQueries,
              graphene.ObjectType):

    pass

SCHEMA = graphene.Schema(query=Queries)
