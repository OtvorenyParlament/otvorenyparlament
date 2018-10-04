"""
Parliament Admin Views
"""

from django.contrib import admin

from parliament.models import Club, Member, MemberChange, Party, Period


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):

    pass


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_select_related = ('stood_for_party', 'person', 'period')
    search_fields = ['person__surname', 'person__forename']
    list_filter = ('period', 'person')


@admin.register(MemberChange)
class MemberChangeAdmin(admin.ModelAdmin):

    list_filter = ('period', 'person')
    list_display = ('period', 'person', 'date', 'change_type')


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):

    pass


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):

    pass
