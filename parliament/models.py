"""
Parliament Models
"""

from datetime import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem

from parliament.choices import DocumentCategory


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


class ClubManaber(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('period')


class Club(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    coalition = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    external_id = models.IntegerField(unique=True, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    objects = ClubManaber()

    class Meta:
        unique_together = (('period', 'name'),)

    def __str__(self):
        return self.name

    @property
    def current_member_count(self):
        today = datetime.utcnow().date()
        return self.members.filter(
            models.Q(start__lte=today),
            models.Q(end__gt=today) | models.Q(end__isnull=True)
        ).count()


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


class MemberManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'person', 'person__residence', 'period', 'stood_for_party'
        ).prefetch_related('active')


class Member(models.Model):
    """
    Member of parliament during election period
    """
    person = models.ForeignKey(
        'person.Person', on_delete=models.CASCADE, related_name='memberships')
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    stood_for_party = models.ForeignKey('Party', on_delete=models.CASCADE)
    url = models.URLField()

    objects = MemberManager()

    class Meta:
        unique_together = (('person', 'period'),)

    def __str__(self):
        return '{}, {}, {}'.format(self.person, self.stood_for_party, self.period)


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
        ordering = ('member', 'start',)


class MemberChange(models.Model):
    """
    Membership changes
    """
    class ChangeType(DjangoChoices):
        mandate_not_applied = ChoiceItem(0, "Mandát sa neuplatňuje")
        active = ChoiceItem(1, "Mandát vykonávaný (aktívny poslanec)")
        substitute_folded = ChoiceItem(2, "Mandát náhradníka zaniknutý")
        substitute_active = ChoiceItem(3, "Mandát náhradníka vykonávaný")
        substitute_gained = ChoiceItem(4, "Mandát náhradníka získaný")
        folded = ChoiceItem(5, "Mandát zaniknutý")
        gained = ChoiceItem(6, "Mandát nadobudnutý vo voľbách")

    person = models.ForeignKey(
        'person.Person', on_delete=models.CASCADE, related_name='changes')
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    date = models.DateField()
    change_type = models.PositiveSmallIntegerField(choices=ChangeType.choices)
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
    NONE = ''

    MEMBERSHIPS = (
        (NONE, 'Žiadny'),
        (CHAIRMAN, 'Predsedníčka/predseda'),
        (VICECHAIRMAN, 'Pod-predsedníčka/predseda'),
        (MEMBER, 'Členka/člen')
    )

    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='members')
    member = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='club_memberships')
    membership = models.CharField(max_length=24, db_index=True, choices=MEMBERSHIPS, default=NONE)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    objects = ClubMemberManager()

    class Meta:
        unique_together = (('club', 'member', 'start'),)
        ordering = ('-start',)

    def __str__(self):
        return '{} - {}'.format(self.club, self.member)

    def end_membership(self):
        """
        Mark current membership as ended
        """
        self.end = timezone.now()
        self.save()
        return True


class PressManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().prefetch_related('votings')


class Press(models.Model):
    """
    Parliament press
    """

    class PressType(DocumentCategory):
        bill = ChoiceItem(1, "Návrh zákona")

    press_type = models.SmallIntegerField(choices=PressType.choices, db_index=True)
    title = models.TextField()
    press_num = models.CharField(max_length=24, db_index=True)
    date = models.DateField(db_index=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='presses')
    url = models.URLField()

    objects = PressManager()

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

    class StateType(DjangoChoices):
        discussed = ChoiceItem(0, "Prerokovaný bod programu")
        notdiscussed = ChoiceItem(1, "Neprerokovaný bod programu")
        moved = ChoiceItem(2, "Presunutý bod programu")
        withdrawn = ChoiceItem(3, "Stiahnutý bod programu")
        interrupted = ChoiceItem(4, "Prerušené rokovanie o bode programu")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='points')
    press = models.ForeignKey(Press, on_delete=models.CASCADE, null=True, blank=True)
    point = models.PositiveSmallIntegerField(null=True, blank=True)
    state = models.SmallIntegerField(choices=StateType.choices)
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
    PASSED = 0
    DID_NOT_PASS = 1
    INQUORATE = 2
    RESULTS = (
        (PASSED, 'Návrh prešiel'),
        (DID_NOT_PASS, 'Návrh neprešiel'),
        (INQUORATE, 'Parlament nebol uznášaniaschopný')
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
    result = models.SmallIntegerField(choices=RESULTS)
    url = models.URLField()
    objects = VotingManager()

    class Meta:
        ordering = ('-voting_num',)

    @property
    def result_display(self):
        return self.get_result_display()

    def chart_series(self):
        display = {
            x[0]: x[1]
            for x in VotingVote._meta.get_field('vote').flatchoices
        }
        sums = self.votes.values('vote').annotate(total=models.Count('vote')).order_by('vote')
        series = []
        labels = []
        for dct in sums:
            labels.append(display[dct['vote']])
            series.append(dct['total'])
        return {'series': series, 'labels': labels}


class VotingVoteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'voter', 'voting', 'voting__session', 'voting__press')


class VotingVote(models.Model):
    FOR = 0
    AGAINST = 1
    ABSTAIN = 2
    DNV = 3
    ABSENT = 4

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
    voter = models.ForeignKey(
        'Member',
        on_delete=models.CASCADE,
        related_name='votes'
    )
    vote = models.SmallIntegerField(choices=OPTIONS)
    objects = VotingVoteManager()

    class Meta:
        ordering = ('-voting__session__session_num', '-voting__voting_num',)
        unique_together = (('voting', 'voter'),)

    def __str__(self):
        return '{} {} {}'.format(self.voting, self.voter, self.vote)


class BillManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('press')


class Bill(models.Model):

    class Category(DocumentCategory):
        pass

    class State(DjangoChoices):
        evidence = ChoiceItem(0, "Evidencia")
        closed_task = ChoiceItem(1, "Uzavretá úloha")
        reading_1 = ChoiceItem(2, "I. čítanie")
        reading_2 = ChoiceItem(3, "II. čítanie")
        reading_3 = ChoiceItem(4, "III. čítanie")
        redaction = ChoiceItem(5, "Redakcia")
        committee_discussion = ChoiceItem(6, "Rokovanie výboru")
        standpoint = ChoiceItem(7, "Stanovisko k NZ")
        council_discussion = ChoiceItem(8, "Rokovanie NR SR")
        coordinator_discussion = ChoiceItem(9, "Rokovanie gestorského výboru")
        advisor_selection = ChoiceItem(10, "Výber poradcov k NZ")

    class Result(DjangoChoices):
        wont_continue = ChoiceItem(0, "NR SR nebude pokračovať v rokovaní o návrhu zákona")
        taken_back = ChoiceItem(1, "NZ vzal navrhovateľ späť")
        resolution_writing = ChoiceItem(2, "Zápis uznesenia NR SR")
        in_redaction = ChoiceItem(3, "NZ postúpil do redakcie")
        committees_report = ChoiceItem(4, "Zápis spoločnej správy výborov")
        wasnot_approved = ChoiceItem(5, "NZ nebol schválený")
        info_ready = ChoiceItem(6, "Pripravená informácia k NZ")
        published = ChoiceItem(7, "Zákon vyšiel v Zbierke zákonov")
        presidential_veto = ChoiceItem(8, "Zákon bol vrátený prezidentom")
        committee_resolution_writing = ChoiceItem(9, "Zapísané uznesenie výboru")
        legal_selection = ChoiceItem(10, "Výber právneho poradcu")
        reading_2 = ChoiceItem(11, "NZ postúpil do II. čítania")

    class Proposer(DjangoChoices):
        members = ChoiceItem(0, "Poslanci NR SR")
        government = ChoiceItem(1, 'Vláda')
        committee = ChoiceItem(2, 'Výbor')

    external_id = models.PositiveIntegerField(unique=True)
    category = models.SmallIntegerField(choices=Category.choices)
    press = models.ForeignKey(Press, on_delete=models.CASCADE)
    delivered = models.DateField(db_index=True)
    proposer_type = models.SmallIntegerField(choices=Proposer.choices, null=True, blank=True)
    proposer_nonmember = models.CharField(max_length=255, default='')
    proposers = models.ManyToManyField(
        Member, related_name='bills', through='BillProposer')
    state = models.SmallIntegerField(choices=State.choices, null=True, blank=True)
    result = models.SmallIntegerField(choices=Result.choices, null=True, blank=True)
    url = models.URLField()

    objects = BillManager()

    class Meta:
        ordering = ('delivered',)


class BillProposer(models.Model):

    bill = models.ForeignKey('Bill', on_delete=models.CASCADE)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('bill', 'member'),)


class BillProcessStep(models.Model):

    class StepType(DjangoChoices):
        registry = ChoiceItem(0, "Podateľňa")
        speaker_resolution = ChoiceItem(1, "Rozhodnutie predsedu NR SR")
        reading_1 = ChoiceItem(2, "I. čítanie")
        committees_discussion = ChoiceItem(3, "Rokovanie výborov")
        coordinator_discussion = ChoiceItem(4, "Rokovanie gestorského výboru")
        reading_2 = ChoiceItem(5, "II. čítanie")
        reading_3 = ChoiceItem(6, "III. čítanie")
        redaction = ChoiceItem(7, "Redakcia")

    class ResultType(DjangoChoices):
        speaker_resolution = ChoiceItem(0, "Zapísané rozhodnutie predsedu NR SR")
        preparing_info = ChoiceItem(1, "Príprava informácie k NZ")
        taken_back = ChoiceItem(2, "NZ vzal navrhovateľ späť")
        wont_continue = ChoiceItem(3, "NR SR nebude pokračovať v rokovaní o návrhu zákona")
        published = ChoiceItem(4, "Zákon vyšiel v Zbierke zákonov.")
        to_redaction = ChoiceItem(5, "NZ postupuje do redakcie")
        reading_1 = ChoiceItem(6, "NZ postúpil do I. čítania")
        reading_2 = ChoiceItem(7, "NZ postúpil do II. čítania")
        reading_3 = ChoiceItem(8, "NZ postúpil do III. čítania")
        committee_resolution_writing = ChoiceItem(9, "Zápis uznesenia / návrhu uznesenia výborov")
        wasnot_approved = ChoiceItem(10, "NZ nebol schválený")
        presidential_veto = ChoiceItem(11, "Zákon bol vrátený prezidentom.")

    STANDPOINT_DISCORDANT = 0
    STANDPOINT_CONFORMABLE = 1

    STANDPOINTS = (
        (STANDPOINT_CONFORMABLE, 'Súhlasný'),
        (STANDPOINT_DISCORDANT, 'Nesúhlasný')
    )
    external_id = models.PositiveIntegerField(unique=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    step_type = models.SmallIntegerField(choices=StepType.choices) # body label
    step_result = models.SmallIntegerField(choices=ResultType.choices)
    meeting_session = models.ForeignKey('Session', on_delete=models.CASCADE)
    meeting_resolution = models.PositiveIntegerField(null=True, blank=True)
    meeting_resolution_date = models.DateField(null=True, blank=True)
    committees_label = models.TextField(default='')
    slk_label = models.TextField(default='')
    coordinator_label = models.TextField(default='')
    coordinator_meeting_date = models.DateField(blank=True, null=True)
    coordinator_name = models.CharField(max_length=255, default='')
    discussed_label = models.CharField(max_length=255, default='')
    sent_standpoint = models.SmallIntegerField(choices=STANDPOINTS)
    sent_label = models.DateField(null=True, blank=True)
    act_num_label = models.CharField(max_length=12)

# class BillAmendment(models.Model):
#     bill_step = models.ForeignKey(BillProcessStep, on_delete=models.CASCADE)
#     date = models.DateField()
#     author = models.ForeignKey(Member, on_delete=models.CASCADE)


# class BillProcessStepAttachment(models.Model):

#     bill_process = models.ForeignKey(BillProcessStep, on_delete=models.CASCADE)
#     title = models.TextField(max_length=512, default='missing title')
#     url = models.URLField()
#     file = models.FilePathField(null=True, blank=True)


class DebateAppearance(models.Model):

    class AppearanceType(DjangoChoices):
        undefined = ChoiceItem(0, "-")
        additional_question = ChoiceItem(1, "Doplňujúca otázka / reakcia zadávajúceho")
        interpellation = ChoiceItem(2, "Prednesenie interpelácie")
        question = ChoiceItem(3, "Prednesenie otázky")
        stating_point = ChoiceItem(4, "Uvádzajúci uvádza bod")
        speaker = ChoiceItem(5, "Vstup predsedajúceho")
        appearance = ChoiceItem(6, "Vystúpenie")
        appearance_fact = ChoiceItem(7, "Vystúpenie s faktickou poznámkou")
        appearance_procedural = ChoiceItem(8, "Vystúpenie s procedurálnym návrhom")
        appearance_correspondent = ChoiceItem(9, "Vystúpenie spoločného spravodajcu")
        debate_appearance = ChoiceItem(10, "Vystúpenie v rozprave")
        answer = ChoiceItem(11, "Zodpovedanie otázky")

    external_id = models.PositiveIntegerField(unique=True)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    start = models.DateTimeField(db_index=True)
    end = models.DateTimeField()
    debater = models.ForeignKey(
        'Member', on_delete=models.CASCADE,
        null=True, blank=True, related_name='debate_appearances')
    appearance_type = models.SmallIntegerField(choices=AppearanceType.choices)
    press_num = models.ManyToManyField('Press', blank=True)
    video_url = models.URLField()
    appearance_addition = models.CharField(max_length=128, default='', blank=True)
    debater_ext = models.CharField(max_length=128, default='', blank=True)
    debater_role = models.TextField(default='', blank=True)
    text = models.TextField(default='', blank=True)

    class Meta:
        ordering = ('external_id',)


class Interpellation(models.Model):

    class StatusType(DjangoChoices):
        awaiting_response = ChoiceItem(0, "Príjem odpovede na interpeláciu")
        debate = ChoiceItem(1, "Rokovanie o interpelácii")
        closed = ChoiceItem(2, "Uzavretá odpoveď na interpeláciu")

    external_id = models.PositiveIntegerField(unique=True)
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    date = models.DateField()
    asked_by = models.ForeignKey(
        'Member', on_delete=models.CASCADE, null=True, blank=True, related_name='interpellations')
    status = models.SmallIntegerField(choices=StatusType.choices)
    interpellation_session = models.ForeignKey(
        'Session', on_delete=models.CASCADE, related_name='interpellations', null=True, blank=True)
    response_session = models.ForeignKey(
        'Session', on_delete=models.CASCADE,
        related_name='interpellation_responses', null=True, blank=True)
    press = models.ForeignKey('Press', on_delete=models.CASCADE, null=True, blank=True)
    responded_by = models.CharField(max_length=64, default='', blank=True)
    recipients = ArrayField(models.CharField(max_length=64))
    url = models.URLField()
    description = models.TextField()

    @property
    def status_display(self):
        return self.get_status_display()


class AmendmentManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('press')


class Amendment(models.Model):

    external_id = models.PositiveIntegerField(unique=True)
    session = models.ForeignKey('Session', on_delete=models.CASCADE, null=True, blank=True)
    press = models.ForeignKey('Press', on_delete=models.CASCADE)
    date = models.DateField()
    voting = models.ForeignKey('Voting', on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField()
    signed_members = models.ManyToManyField(
        'Member',
        related_name='signed_amendments',
        through='AmendmentSignedMember',
        blank=True)
    submitters = models.ManyToManyField(
        'Member',
        related_name='submitted_amendments',
        through='AmendmentSubmitter',
        blank=True)

    objects = AmendmentManager()


class AmendmentSignedMember(models.Model):

    amendment = models.ForeignKey('Amendment', on_delete=models.CASCADE)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('amendment', 'member'),)


class AmendmentSubmitter(models.Model):

    amendment = models.ForeignKey('Amendment', on_delete=models.CASCADE)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    main = models.BooleanField(default=False)

    class Meta:
        unique_together = (('amendment', 'member'), ('amendment', 'main'))
