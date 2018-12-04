"""
GraphQL interface to Django flatpages
"""

from django.contrib.flatpages.models import FlatPage

import graphene
from graphene.types import ObjectType


class FlatPageType(ObjectType):

    title = graphene.String()
    content = graphene.String()
    url = graphene.String()


class FlatPageQueries(ObjectType):

    flat_page = graphene.Field(FlatPageType, url=graphene.String(required=True))

    def resolve_flat_page(self, info, url):
        try:
            page = FlatPage.objects.get(url=url)
        except FlatPage.DoesNotExist:
            raise Exception("Page not found")

        return FlatPageType(url=url, title=page.title, content=page.content)
