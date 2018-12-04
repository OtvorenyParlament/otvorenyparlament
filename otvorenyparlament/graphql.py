"""
GraphQL Schema
"""

import graphene

from flatpages_api.graphql import FlatPageQueries
from geo.graphql import GeoQueries
from parliament.graphql import ParliamentQueries
from parliament_stats.graphql import ParliamentStatsQueries
from person.graphql import PersonQueries


class Queries(FlatPageQueries, GeoQueries, ParliamentQueries, ParliamentStatsQueries,
              PersonQueries, graphene.ObjectType):

    pass

SCHEMA = graphene.Schema(query=Queries)
