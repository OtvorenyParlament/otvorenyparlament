"""
GraphQL Schema
"""

import graphene

from parliament.graphql import ParliamentQueries


class Queries(ParliamentQueries, graphene.ObjectType):

    pass

SCHEMA = graphene.Schema(query=Queries)
