"""
GraphQL Schema
"""

import graphene

from geo.graphql import GeoQueries
from parliament.graphql import ParliamentQueries


class Queries(GeoQueries, ParliamentQueries, graphene.ObjectType):

    pass

SCHEMA = graphene.Schema(query=Queries)
