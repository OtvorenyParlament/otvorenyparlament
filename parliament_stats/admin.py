from django.contrib import admin

from parliament_stats.models import ClubStats

@admin.register(ClubStats)
class ClubStatsAdmin(admin.ModelAdmin):
    list_display = ('date', 'club')
    list_filter = ('date', 'club')
