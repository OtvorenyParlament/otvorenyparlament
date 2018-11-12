"""
Aggregated stats from parliament app
"""

from django.db import models


class ClubStats(models.Model):

    club = models.ForeignKey('parliament.Club', on_delete=models.CASCADE)
    date = models.DateField()
    # bills
    bill_coalition = models.PositiveSmallIntegerField()
    bill_opposition = models.PositiveSmallIntegerField()
    # amendments
    amendment_coalition = models.PositiveSmallIntegerField()
    amendment_opposition = models.PositiveSmallIntegerField()
    # debate appearances
    debate_count_coalition = models.PositiveSmallIntegerField()
    debate_count_opposition = models.PositiveSmallIntegerField()
    debate_member_count = models.PositiveSmallIntegerField()
    debate_seconds_coalition = models.PositiveSmallIntegerField()
    debate_seconds_opposition = models.PositiveSmallIntegerField()
    # interpelations
    interpelation_coalition = models.PositiveSmallIntegerField()
    interpelation_opposition = models.PositiveSmallIntegerField()
    # votings
    voting_coalition_for = models.PositiveSmallIntegerField()
    voting_coalition_against = models.PositiveSmallIntegerField()
    voting_coalition_abstain = models.PositiveSmallIntegerField()
    voting_coalition_dnv = models.PositiveSmallIntegerField()
    voting_coalition_absent = models.PositiveSmallIntegerField()

    voting_opposition_for = models.PositiveSmallIntegerField()
    voting_opposition_against = models.PositiveSmallIntegerField()
    voting_opposition_abstain = models.PositiveSmallIntegerField()
    voting_opposition_dnv = models.PositiveSmallIntegerField()
    voting_opposition_absent = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('club', 'date',))
        verbose_name = 'Club Stats'
        verbose_name_plural = verbose_name
