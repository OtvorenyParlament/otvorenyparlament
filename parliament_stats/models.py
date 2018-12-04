"""
Aggregated stats from parliament app
"""

from django.db import models


class GlobalStats(models.Model):

    period = models.ForeignKey(
        'parliament.Period', on_delete=models.CASCADE, related_name='global_stats')
    date = models.DateField(unique=True)
    bill_count_by_coalition = models.PositiveSmallIntegerField()
    bill_count_by_opposition = models.PositiveSmallIntegerField()
    amendment_count_by_coalition = models.PositiveSmallIntegerField()
    amendment_count_by_opposition = models.PositiveSmallIntegerField()
    interpellation_count_by_coalition = models.PositiveSmallIntegerField()
    interpellation_count_by_opposition = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('period', 'date',))
        verbose_name = 'Global Stats'
        verbose_name_plural = verbose_name


class ClubStats(models.Model):

    club = models.ForeignKey(
        'parliament.Club', on_delete=models.CASCADE, related_name='club_stats')
    date = models.DateField()
    # bills
    bill_count = models.PositiveSmallIntegerField()
    # amendments
    amendment_coalition = models.PositiveSmallIntegerField()
    amendment_opposition = models.PositiveSmallIntegerField()
    amendment_government = models.PositiveSmallIntegerField()
    amendment_committee = models.PositiveSmallIntegerField()
    # debate appearances
    debater_count_coalition = models.PositiveSmallIntegerField()
    debater_count_opposition = models.PositiveSmallIntegerField()
    debater_count_committee = models.PositiveSmallIntegerField()
    debater_count_government = models.PositiveSmallIntegerField()
    debate_count_coalition = models.PositiveSmallIntegerField()
    debate_count_opposition = models.PositiveSmallIntegerField()
    debate_count_government = models.PositiveSmallIntegerField()
    debate_count_committee = models.PositiveSmallIntegerField()
    debate_seconds_coalition = models.PositiveSmallIntegerField()
    debate_seconds_opposition = models.PositiveSmallIntegerField()
    debate_seconds_government = models.PositiveSmallIntegerField()
    debate_seconds_committee = models.PositiveSmallIntegerField()
    # interpellations
    interpellation_count = models.PositiveSmallIntegerField()
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

    voting_government_for = models.PositiveSmallIntegerField()
    voting_government_against = models.PositiveSmallIntegerField()
    voting_government_abstain = models.PositiveSmallIntegerField()
    voting_government_dnv = models.PositiveSmallIntegerField()
    voting_government_absent = models.PositiveSmallIntegerField()

    voting_committee_for = models.PositiveSmallIntegerField()
    voting_committee_against = models.PositiveSmallIntegerField()
    voting_committee_abstain = models.PositiveSmallIntegerField()
    voting_committee_dnv = models.PositiveSmallIntegerField()
    voting_committee_absent = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('club', 'date',))
        verbose_name = 'Club Stats'
        verbose_name_plural = verbose_name


class MemberStats(models.Model):

    member = models.ForeignKey(
        'parliament.Member', on_delete=models.CASCADE, related_name='member_stats')
    date = models.DateField()
    bill_count = models.PositiveSmallIntegerField()
    amendment_count = models.PositiveSmallIntegerField()
    interpellation_count = models.PositiveSmallIntegerField()
    debate_count = models.PositiveSmallIntegerField()
    debate_seconds = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (('member', 'date',))
        verbose_name = 'MP Stats'
        verbose_name_plural = verbose_name
