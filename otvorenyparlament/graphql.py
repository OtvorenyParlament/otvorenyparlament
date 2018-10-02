"""
GraphQL Schema
"""

import graphene


class Queries(graphene.ObjectType):

    pass

SCHEMA = graphene.Schema(query=Queries)
