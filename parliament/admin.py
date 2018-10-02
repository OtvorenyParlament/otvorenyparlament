"""
Parliament Admin Views
"""

from django.contrib import admin


from parliament.models import Club, Period


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):

    pass


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):

    pass
