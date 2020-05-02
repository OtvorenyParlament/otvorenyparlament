"""
GraphQL Common utils
"""

from functools import partial

from django.db.models import F, Q
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id
from promise import Promise


class OrderedDjangoFilterConnectionField(DjangoFilterConnectionField):
    """Orderable DjangoFilterConnectionField"""


    @classmethod
    def connection_resolver(cls, resolver, connection, default_manager,
                            queryset_resolver, max_limit,
                            enforce_first_or_last, root, info, **args):
        first = args.get("first")
        last = args.get("last")

        if enforce_first_or_last:
            assert first or last, (
                "You must provide a `first` or `last` value to properly paginate the `{}` connection."
            ).format(info.field_name)

        if max_limit:
            if first:
                assert first <= max_limit, (
                    "Requesting {} records on the `{}` connection exceeds the `first` limit of {} records."
                ).format(first, info.field_name, max_limit)
                args["first"] = min(first, max_limit)

            if last:
                assert last <= max_limit, (
                    "Requesting {} records on the `{}` connection exceeds the `last` limit of {} records."
                ).format(last, info.field_name, max_limit)
                args["last"] = min(last, max_limit)

        # eventually leads to DjangoObjectType's get_queryset (accepts queryset)
        # or a resolve_foo (does not accept queryset)
        iterable = resolver(root, info, **args)
        if iterable is None:
            iterable = default_manager
        # thus the iterable gets refiltered by resolve_queryset
        # but iterable might be promise
        iterable = queryset_resolver(connection, iterable, info, args)

        club = args.get('club', None)
        customized_club_filters = [
            'all_amendments', 'all_interpellations', 'all_debate_appearances']
        current_resolver = resolver.args[0]
        if club and current_resolver in customized_club_filters:
            id_tuple = from_global_id(club)
            if id_tuple[0] == 'ClubType':
                dfilter_key = 'date'
                if current_resolver == 'all_amendments':
                    filter_key = 'submitters'
                elif current_resolver == 'all_interpellations':
                    filter_key = 'asked_by'
                elif current_resolver == 'all_debate_appearances':
                    filter_key = 'debater'
                    dfilter_key = 'start'
                iterable = iterable.filter(
                    Q(**{'{}__club_memberships__club__id'.format(filter_key): id_tuple[1]}) &
                    Q(**{'{}__club_memberships__start__lte'.format(filter_key): F(dfilter_key)}) &
                    (
                        Q(**{'{}__club_memberships__end__gte'.format(filter_key): F(dfilter_key)}) |
                        Q(**{'{}__club_memberships__end__isnull'.format(filter_key): True})
                    )
                ).distinct()

        order = args.get('orderBy', None)
        if order:
            iterable = iterable.order_by(*order)

        on_resolve = partial(cls.resolve_connection, connection, args)

        if Promise.is_thenable(iterable):
            return Promise.resolve(iterable).then(on_resolve)

        return on_resolve(iterable)


class CountableConnectionBase(graphene.relay.Connection):
    """Adds totalCount to type lists"""

    class Meta:
        abstract = True

    total_count = graphene.Int()
    def resolve_total_count(self, info, **kwargs):
        print(self.iterable.explain(verbose=True))
        print(self.iterable.query)
        print("PES")
        return self.iterable.count()
