"""
Parliament Models
"""

from django.db import models
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
