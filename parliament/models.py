"""
Parliament Models
"""

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Period(models.Model):
    period_num = models.PositiveIntegerField(verbose_name=_('Period number'))
    year_start = models.SmallIntegerField()
    year_end = models.SmallIntegerField(null=True, blank=True)
    snap_end = models.BooleanField(default=False)

    class Meta:
        ordering = ('-period_num',)

    def __str__(self):
        return '{}: {} - {}'.format(
            self.period_num, self.year_start, self.year_end or '')


class Club(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    external_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Party(models.Model):
    """
    Parliament Party
    """
    name = models.CharField(max_length=255, verbose_name=_('Party'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Parties')


class Member(models.Model):
    """
    Member of parliament during election period
    """
    person = models.ForeignKey(
        'person.Person', on_delete=models.CASCADE, related_name='memberships')
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    stood_for_party = models.ForeignKey('Party', on_delete=models.CASCADE)
    start = models.DateField(default=timezone.now)
    end = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.person, self.stood_for_party, self.period)

    @property
    def is_active(self):
        today = timezone.now().date
        date_period = Period.objects.get(start_date__gte=today, end_date__lt=today)
        change = self.person.changes.filter(period=date_period).order_by('-date').first()
        if change.change_type == MemberChange.ACTIVE:
            return True
        return False


class MemberChange(models.Model):
    """
    Membership changes
    """

    MANDATE_NOT_APPLIED = 'mandatenotapplied'
    ACTIVE = 'active'
    SUBSTITUTE_FOLDED = 'substitutefolded'
    SUBSTITUTE_ACTIVE = 'substituteactive'
    SUBSTITUTE_GAINED = 'substitutegained'
    FOLDED = 'folded'
    GAINED = 'gained'

    CHANGE_TYPES = (
        (MANDATE_NOT_APPLIED, "Mandát sa neuplatňuje"),
        (ACTIVE, "Mandát vykonávaný (aktívny poslanec)"),
        (SUBSTITUTE_FOLDED, "Mandát náhradníka zaniknutý"),
        (SUBSTITUTE_ACTIVE, "Mandát náhradníka vykonávaný"),
        (SUBSTITUTE_GAINED, "Mandát náhradníka získaný"),
        (FOLDED, "Mandát zaniknutý"),
        (GAINED, "Mandát nadobudnutý vo voľbách")
    )

    person = models.ForeignKey(
        'person.Person', on_delete=models.CASCADE, related_name='changes')
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    date = models.DateField()
    change_type = models.CharField(max_length=64, choices=CHANGE_TYPES)
    change_reason = models.TextField()


class Press(models.Model):
    """
    Parliament press
    """
    TYPE_OTHER = 'other'
    TYPE_INT_AGREEMENT = 'intag'
    TYPE_PETITION = 'petition'
    TYPE_INFORMATION = 'information'
    TYPE_DRAFTLAW = 'draftlaw'
    TYPE_REPORT = 'report'
    TYPES = (
        (TYPE_OTHER, _('Other type')),
        (TYPE_INT_AGREEMENT, _('International agreement')),
        (TYPE_PETITION, _('Petition')),
        (TYPE_INFORMATION, _('Information')),
        (TYPE_DRAFTLAW, _('Draft law')),
        (TYPE_REPORT, _('Report')),
    )
    external_id = models.IntegerField(null=True, blank=True)
    press_type = models.CharField(max_length=24, choices=TYPES, db_index=True)
    title = models.TextField()
    press_num = models.CharField(max_length=24, db_index=True)
    date = models.DateField(db_index=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='presses')
    url = models.URLField()

    class Meta:
        verbose_name = _('press')
        verbose_name_plural = _('presses')

    def __str__(self):
        return self.title


class PressAttachment(models.Model):
    title = models.TextField(max_length=512, default='missing title')
    press = models.ForeignKey(Press, on_delete=models.CASCADE, related_name='attachments')
    url = models.URLField()
    file = models.FilePathField(null=True, blank=True)

    def __str__(self):
        return self.title
