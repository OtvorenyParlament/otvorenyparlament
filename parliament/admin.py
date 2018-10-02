"""
Parliament Admin Views
"""

from django.contrib import admin


from parliament.models import Period

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):

    pass
