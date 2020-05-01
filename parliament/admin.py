"""
Parliament Admin Views
"""

from django.contrib import admin

from parliament.models import (Bill, BillProcessStep, Club, ClubMember,
                               Committee, CommitteeMember, Interpellation, Member,
                               MemberActive, MemberChange, Party, Period,
                               Press, Session, Voting, VotingVote)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):

    list_display = ('get_period', 'external_id', 'category', 'delivered')
    list_filter = ('proposers__club_memberships__club', 'press__period')

    def get_period(self, obj):
        return obj.press.period
    get_period.short_description = 'Period'
    get_period.admin_order_field = 'press__period'


@admin.register(BillProcessStep)
class BillStepProcessAdmin(admin.ModelAdmin):

    pass


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):

    list_display = ('period', 'name', 'coalition')


@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):

    list_filter = ('club', 'member__period',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "club":
            kwargs["queryset"] = Club.objects.all().select_related()
        if db_field.name == 'member':
            kwargs['queryset'] = Member.objects.all(
            ).select_related().prefetch_related().order_by(
                'person__forename', 'person__surname')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('name', 'period')
    list_filter = ('period',)


@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('member', 'committee', 'membership')
    list_filter = ('committee', 'membership')


@admin.register(Interpellation)
class InterpellationAdmin(admin.ModelAdmin):
    list_display = ['external_id', 'period', 'date', 'asked_by']
    list_filter = ['period', 'asked_by']
    search_fields = ['external_id', 'asked_by', 'press']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    list_select_related = ('stood_for_party', 'person', 'period')
    search_fields = ['person__surname', 'person__forename']
    list_filter = ('period', 'person')


@admin.register(MemberActive)
class MemberActiveAdmin(admin.ModelAdmin):

    list_display = ('member', 'start', 'end')

@admin.register(MemberChange)
class MemberChangeAdmin(admin.ModelAdmin):

    list_filter = ('period', 'person', 'change_type')
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
    list_display = ('period', 'date', 'press_type', 'press_num', 'title')
    search_fields = ['press_num']
    list_filter = ('period',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):

    list_display = ('period', 'name', 'session_num', 'external_id')


class VotingVoteInline(admin.TabularInline):

    model = VotingVote


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    inlines = [VotingVoteInline,]
    list_display = ('external_id', 'voting_num', 'topic', 'timestamp', 'result')
    list_filter = ('session', 'result')
