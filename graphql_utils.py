"""
GraphQL Common utils
"""

import graphene
from graphene_django.filter import DjangoFilterConnectionField


class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):
    """Orderable DjangoFilterConnectionField"""

    @classmethod
    def connection_resolver(cls, resolver, connection, default_manager,
                            max_limit, enforce_first_or_last, filterset_class,
                            filtering_args, root, info, **args):
        filter_kwargs = {k: v for k, v in args.items() if k in filtering_args}
        qs = default_manager.get_queryset() if hasattr(
            default_manager, 'get_queryset') else default_manager
        qs = filterset_class(data=filter_kwargs, queryset=qs).qs
        order = args.get('orderBy', None)
        if order:
            qs = qs.order_by(*order)
        return super(DjangoFilterConnectionField, cls).connection_resolver(
            resolver, connection, qs, max_limit, enforce_first_or_last, root,
            info, **args)


class CountableConnectionBase(graphene.relay.Connection):
    """Adds totalCount to type lists"""

    class Meta:
        abstract = True

    total_count = graphene.Int()
    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()
