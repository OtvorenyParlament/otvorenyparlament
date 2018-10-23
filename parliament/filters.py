"""
Parliament filters
"""

from django.db.models import Q
from django.utils import timezone
import django_filters

from parliament.models import Member, MemberChange, Period, VotingVote


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

    class Meta:
        model = VotingVote
        fields = {
            'id': ('exact',),
            'voting__voting_num': ('exact',),
            'voting__session__session_num': ('exact',),
            'voting__session__period__period_num': ('exact',),
            'person': ('exact',)
        }

    @property
    def qs(self):
        parent = super().qs
        return parent
