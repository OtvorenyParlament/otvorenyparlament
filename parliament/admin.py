"""
Parliament Admin Views
"""

from django.contrib import admin

from parliament.models import (Club, ClubMember, Member, MemberChange, Party,
                               Period, Press, Session, Voting, VotingVote)


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):

    pass


@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):

    list_filter = ('club',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "club":
            kwargs["queryset"] = Club.objects.all().select_related()
        if db_field.name == 'member':
            kwargs['queryset'] = Member.objects.all(
            ).select_related().prefetch_related().order_by(
                'person__forename', 'person__surname')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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


@admin.register(Press)
class PressAdmin(admin.ModelAdmin):

    list_select_related = ('period',)
    list_display = ('period', 'press_type', 'press_num', 'title')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):

    list_display = ('period', 'name', 'session_num', 'external_id')


class VotingVoteInline(admin.TabularInline):

    model = VotingVote


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    inlines = [VotingVoteInline,]
