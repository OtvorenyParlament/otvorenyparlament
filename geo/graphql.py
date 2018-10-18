"""
Geo GraphQL Queries
"""

import graphene
from graphene_django import DjangoObjectType

from graphql_utils import CountableConnectionBase, OrderedDjangoFilterConnectionField

from geo.models import Region, District, Village


class RegionType(DjangoObjectType):

    """SK Regions"""

    class Meta:
        interfaces = (graphene.relay.Node,)
        model = Region
        connection_class = CountableConnectionBase
        filter_fields = {
            'shortcut': ['exact'],
        }


class DistrictType(DjangoObjectType):

    """SK Districts"""

    class Meta:
        interfaces = (graphene.relay.Node,)
        model = District
        connection_class = CountableConnectionBase
        filter_fields = {
            'name': ['exact', 'icontains'],
            'region__name': ['exact', 'icontains'],
            'region__shortcut': ['exact'],
        }


class VillageType(DjangoObjectType):

    """SK Villages"""

    class Meta:
        interfaces = (graphene.relay.Node,)
        model = Village
        connection_class = CountableConnectionBase
        filter_fields = {
            'full_name': ['exact', 'icontains'],
            'district__name': ['exact', 'icontains'],
            'district__region__name': ['exact', 'icontains'],
            'district__region__shortcut': ['exact'],
        }

class GeoQueries(graphene.ObjectType):

    region = graphene.relay.Node.Field(RegionType)
    all_regions = OrderedDjangoFilterConnectionField(RegionType)

    district = graphene.relay.Node.Field(DistrictType)
    all_districts = OrderedDjangoFilterConnectionField(DistrictType)

    village = graphene.relay.Node.Field(VillageType)
    all_villages = OrderedDjangoFilterConnectionField(VillageType)
