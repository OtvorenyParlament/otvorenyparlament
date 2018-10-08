"""
Parliament filters
"""

import django_filters

from parliament.models import VotingVote


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
