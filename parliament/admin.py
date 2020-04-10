"""
Parliament Admin Views
"""

from django.contrib import admin

from parliament.models import (Bill, BillProcessStep, Club, ClubMember,
                               Committee, CommitteeMember, Member,
                               MemberActive, MemberChange, Party, Period,
                               Press, Session, Voting, VotingVote)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):

    list_display = ('external_id',)
    list_filter = ('proposers__club_memberships__club',)


@admin.register(BillProcessStep)
class BillStepProcessAdmin(admin.ModelAdmin):

    pass


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):

    list_display = ('period', 'name', 'coalition')


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


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('name', 'period')
    list_Filter = ('period',)


@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    pass


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
    list_display = ('period', 'press_type', 'press_num', 'title')
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
