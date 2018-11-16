"""
GraphQL Schema
"""

import graphene

from geo.graphql import GeoQueries
from parliament.graphql import ParliamentQueries
from parliament_stats.graphql import ParliamentStatsQueries
from person.graphql import PersonQueries


class Queries(GeoQueries, ParliamentQueries, ParliamentStatsQueries, PersonQueries,
              graphene.ObjectType):

    pass

SCHEMA = graphene.Schema(query=Queries)
