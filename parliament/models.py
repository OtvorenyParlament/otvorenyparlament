"""
Parliament Models
"""

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Period(models.Model):
    period_num = models.PositiveIntegerField(verbose_name=_('Period number'))
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    snap_end = models.BooleanField(default=False)

    class Meta:
        ordering = ('-period_num',)

    def __str__(self):
        return '{}: {} - {}'.format(
            self.period_num, self.start_date, self.end_date or '')


class Club(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    external_id = models.IntegerField(unique=True)
    url = models.URLField()

    def __str__(self):
        return self.name


class Party(models.Model):
    """
    Parliament Party
    """
    # TODO(Jozef): Parties are duplicated in some periods with different
    # names, also some changed name in time. Improve this model
    name = models.CharField(max_length=255, verbose_name=_('Party'), unique=True)

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
    url = models.URLField()

    class Meta:
        unique_together = (('person', 'period'),)

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


class MemberActive(models.Model):
    """
    Member active periods
    """
    member = models.ForeignKey(
        'Member', on_delete=models.CASCADE, related_name='active')
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = (('member', 'start'),)


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

    class Meta:
        unique_together = (('person', 'period', 'date', 'change_type'),)


class ClubMemberManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('club', 'member', 'member__person')


class ClubMember(models.Model):

    CHAIRMAN = 'chairman'
    VICECHAIRMAN = 'vice-chairman'
    MEMBER = 'member'

    MEMBERSHIPS = (
        (CHAIRMAN, 'Predsedníčka/predseda'),
        (VICECHAIRMAN, 'Pod-predsedníčka/predseda'),
        (MEMBER, 'Členka/člen')
    )

    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    member = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='club_memberships')
    membership = models.CharField(max_length=24, db_index=True, choices=MEMBERSHIPS)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    objects = ClubMemberManager()

    class Meta:
        unique_together = (('club', 'member', 'membership'),)

    def __str__(self):
        return '{} - {}'.format(self.club, self.member)

    def end_membership(self):
        """
        Mark current membership as ended
        """
        self.end = timezone.now()
        self.save()
        return True


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
    press_type = models.CharField(max_length=24, choices=TYPES, db_index=True)
    title = models.TextField()
    press_num = models.CharField(max_length=24, db_index=True)
    date = models.DateField(db_index=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='presses')
    url = models.URLField()

    class Meta:
        verbose_name = _('press')
        verbose_name_plural = _('presses')
        unique_together = (('press_num', 'period'),)

    def __str__(self):
        return self.title


class PressAttachment(models.Model):
    title = models.TextField(max_length=512, default='missing title')
    press = models.ForeignKey(Press, on_delete=models.CASCADE, related_name='attachments')
    url = models.URLField()
    file = models.FilePathField(null=True, blank=True)

    def __str__(self):
        return self.title


class Session(models.Model):
    """
    Parliament Sessions
    """
    name = models.CharField(max_length=255)
    external_id = models.PositiveIntegerField(unique=True)
    period = models.ForeignKey('Period', on_delete=models.CASCADE, related_name='sessions')
    session_num = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField()

    class Meta:
        ordering = ('-period', '-session_num')

    def __str__(self):
        return self.name


class SessionProgram(models.Model):
    """
    Parliament Session Program
    """
    DISCUSSED = 'discussed'
    NOTDISCUSSED = 'notdiscussed'
    MOVED = 'moved'
    WITHDRAWN = 'withdrawn'
    INTERRUPTED = 'interrupted'

    STATES = (
        (DISCUSSED, "Prerokovaný bod programu"),
        (NOTDISCUSSED, "Neprerokovaný bod programu"),
        (MOVED, "Presunutý bod programu"),
        (WITHDRAWN, "Stiahnutý bod programu"),
        (INTERRUPTED, "Prerušené rokovanie o bode programu")
    )

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='points')
    press = models.ForeignKey(Press, on_delete=models.CASCADE, null=True, blank=True)
    point = models.PositiveIntegerField(null=True, blank=True)
    state = models.CharField(max_length=24, choices=STATES)
    text1 = models.TextField(default='', blank=True)
    text2 = models.TextField(default='', blank=True)
    text3 = models.TextField(default='', blank=True)

    class Meta:
        ordering = ('session', 'point')

    def __str__(self):
        return '{}. {}'.format(self.point, self.text1)


class SessionAttachment(models.Model):
    """
    Parliament Session Attachments
    """
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attachments')
    title = models.TextField(max_length=512, default='missing title')
    url = models.URLField()

    def __str__(self):
        return '{} {}'.format(self.session, self.title)


class VotingManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('session', 'press')


class Voting(models.Model):
    PASSED = 'passed'
    DID_NOT_PASS = 'did_not_pass'
    PARLIAMENT_UNABLE = 'parliament_unable'
    RESULTS = (
        (PASSED, 'Návrh prešiel'),
        (DID_NOT_PASS, 'Návrh neprešiel'),
        (PARLIAMENT_UNABLE, 'Parlament nebol uznášaniaschopný')
    )
    external_id = models.PositiveIntegerField(unique=True)
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='votings')
    press = models.ForeignKey(
        Press,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='votings')
    voting_num = models.PositiveIntegerField()
    topic = models.TextField()
    timestamp = models.DateTimeField()
    result = models.CharField(max_length=24, choices=RESULTS)
    url = models.URLField()
    objects = VotingManager()

    class Meta:
        ordering = ('-voting_num',)

    # @property
    def chart_series(self):
        display = {
            x[0]: x[1]
            for x in VotingVote._meta.get_field('vote').flatchoices
        }
        sums = self.votes.values('vote').annotate(total=models.Count('vote'))
        series = []
        labels = []
        for dct in sums:
            labels.append(display[dct['vote']])
            series.append(dct['total'])
        return {'series': series, 'labels': labels}


class VotingVoteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'person', 'voting', 'voting__session', 'voting__press')


class VotingVote(models.Model):
    FOR = 'Z'
    AGAINST = 'P'
    ABSTAIN = '?'
    DNV = 'N'
    ABSENT = '0'

    OPTIONS = (
        (FOR, 'Za'),
        (AGAINST, 'Proti'),
        (ABSTAIN, 'Zdržal(a) sa'),
        (DNV, 'Nehlasoval(a)'),
        (ABSENT, 'Neprítomná/ý')
        # (FOR, _('for')),
        # (AGAINST, _('against')),
        # (ABSTAIN, _('abstained')),
        # (DNV, _('did not vote')),
        # (ABSENT, _('absent'))
    )

    voting = models.ForeignKey(
        Voting, on_delete=models.CASCADE, related_name='votes')
    person = models.ForeignKey(
        'person.Person',
        on_delete=models.CASCADE,
        related_name='votes',
        null=True,
        blank=True)
    vote = models.CharField(max_length=4, choices=OPTIONS)
    objects = VotingVoteManager()

    class Meta:
        ordering = ('-voting__session__session_num', '-voting__voting_num',)
        unique_together = (('voting', 'person'),)

    def __str__(self):
        return '{} {} {}'.format(self.voting, self.person, self.vote)
