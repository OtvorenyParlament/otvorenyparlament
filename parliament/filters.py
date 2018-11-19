"""
Parliament filters
"""

from django.db.models import F, Q
from django.utils import timezone
import django_filters
from django_filters.conf import settings as filter_settings
from django_filters.constants import EMPTY_VALUES

from graphql_relay.node.node import from_global_id

from parliament.models import Amendment, AmendmentSubmitter, Bill, Club, ClubMember, Member, MemberChange, Period, VotingVote


class AmendmentFilterSet(django_filters.FilterSet):

    # club = django_filters.CharFilter(method='filter_club')

    class Meta:
        model = Amendment
        fields = {
            'external_id': ('exact',),
            'session': ('exact',),
            'session__period': ('exact',),
            'press': ('exact',),
            'voting': ('exact',),
            'date': ('exact',),
        }

    # FIXME: see FIXME in graphql_utils connection_resolver
    # def filter_club(self, queryset, name, value):
    #     id_tuple = from_global_id(value)
    #     queryset = queryset.filter(
    #         Q(submitters__club_memberships__club__id=id_tuple[1]) &
    #         Q(submitters__club_memberships__start__lte=F('date')) &
    #         (
    #             Q(submitters__club_memberships__end__gte=F('date')) |
    #             Q(submitters__club_memberships__end__isnull=True)
    #         )
    #     ).distinct()

    #     return queryset


class BillFilterSet(django_filters.FilterSet):

    class Meta:
        model = Bill
        fields = {
            'external_id': ('exact',),
            'category': ('exact',),
            'press': ('exact',),
            'press__period': ('exact',),
            'press__period__period_num': ('exact',),
            'delivered': ('exact',),
            'state': ('exact',),
            'result': ('exact',),
            'proposers__club_memberships__club': ('exact',)
        }

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.distinct()


class ClubMemberFilterSet(django_filters.FilterSet):

    is_current_member = django_filters.DateFilter(
        field_name='is_current_member', method='filter_is_current_member')

    def filter_is_current_member(self, queryset, name, value):
        queryset = queryset.filter(
            Q(start__lte=value),
            Q(end__gt=value) | Q(end__isnull=True)
        )
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.distinct()

    class Meta:
        model = ClubMember
        fields = {
            'id': ('exact',),
            'club': ('exact',),
            'club__name': ('exact', 'icontains'),
            'member__period__period_num': ('exact',),
        }


class MemberFilterSet(django_filters.FilterSet):

    is_active = django_filters.DateFilter(field_name='is_active', method='filter_is_active')

    def filter_is_active(self, queryset, name, value):
        queryset = queryset.filter(
            Q(active__start__lte=value),
            Q(active__end__gt=value) | Q(active__end__isnull=True)
        )
        return queryset


    class Meta:
        model = Member
        fields = {
            'id': ('exact',),
            'stood_for_party': ('exact',),
            'period__period_num': ('exact',),
            'person__id': ('exact',)
        }


class VotingVoteFilterSet(django_filters.FilterSet):

    exclude_for = django_filters.BooleanFilter(
        field_name='exclude_for', method='filter_exclude_for')
    exclude_against = django_filters.BooleanFilter(
        field_name='exclude_against', method='filter_exclude_against')
    exclude_abstain = django_filters.BooleanFilter(
        field_name='exclude_abstain', method='filter_exclude_abstain')
    exclude_dnv = django_filters.BooleanFilter(
        field_name='exclude_dnv', method='filter_exclude_dnv')
    exclude_absent = django_filters.BooleanFilter(
        field_name='exclude_absent', method='filter_exclude_absent')

    def filter_exclude_for(self, queryset, name, value):
        if value is True:
            queryset = queryset.exclude(vote=VotingVote.FOR)
        return queryset

    def filter_exclude_against(self, queryset, name, value):
        if value is True:
            queryset = queryset.exclude(vote=VotingVote.AGAINST)
        return queryset

    def filter_exclude_abstain(self, queryset, name, value):
        if value is True:
            queryset = queryset.exclude(vote=VotingVote.ABSTAIN)
        return queryset

    def filter_exclude_dnv(self, queryset, name, value):
        if value is True:
            queryset = queryset.exclude(vote=VotingVote.DNV)
        return queryset

    def filter_exclude_absent(self, queryset, name, value):
        if value is True:
            queryset = queryset.exclude(vote=VotingVote.ABSENT)
        return queryset

    class Meta:
        model = VotingVote
        fields = {
            'id': ('exact',),
            'voting__voting_num': ('exact',),
            'voting__session': ('exact',),
            'voting__session__session_num': ('exact',),
            'voting__session__period__period_num': ('exact',),
            'voter': ('exact',),
            'voter__person': ('exact',)
        }

    @property
    def qs(self):
        parent = super().qs
        return parent
