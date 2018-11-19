"""
GraphQL Common utils
"""

from django.db.models import F, Q
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id


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
        # FIXME: the club stuff is a workaround of django-filter generating
        # duplicated INNER JOINS while filtering on m2m. Another option is to just
        # generate CharFilter with custom method and force it to be a graphene.ID
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
                qs = qs.filter(
                    Q(**{'{}__club_memberships__club__id'.format(filter_key): id_tuple[1]}) &
                    Q(**{'{}__club_memberships__start__lte'.format(filter_key): F(dfilter_key)}) &
                    (
                        Q(**{'{}__club_memberships__end__gte'.format(filter_key): F(dfilter_key)}) |
                        Q(**{'{}__club_memberships__end__isnull'.format(filter_key): True})
                    )
                ).distinct()
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
