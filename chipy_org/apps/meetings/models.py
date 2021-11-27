from __future__ import unicode_literals

import datetime
import random
import string

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from tinymce import models as tinymce_models

from chipy_org.libs.models import CommonModel

from .email import send_rsvp_email

MAX_LENGTH = 255

MEETING = (
    ("Loop", "Loop Meeting - 2nd Thursday"),
    ("North", "North Meeting - 3rd Thursday"),
)


class Venue(CommonModel):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=MAX_LENGTH)
    email = models.EmailField(max_length=MAX_LENGTH, blank=True, null=True)
    phone = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def get_latitude(self):
        raise NotImplementedError

    def get_longitude(self):
        raise NotImplementedError

    longitude = property(get_longitude)
    latitude = property(get_latitude)

    @property
    def jsonLatLng(self):  # pylint: disable=invalid-name
        """
        Use the string returned as args for google.maps.LatLng constructor.
        """
        if self.latitude is not None and self.longitude is not None:
            return f"{self.latitude:.6f},{self.longitude:.6f}"

    directions = models.TextField(blank=True, null=True)
    embed_map = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)


class MeetingType(CommonModel):
    """
    This model contains entries for different meeting types.
    Example:
      - SIG Meetings
      - Mentorship Meetings
      - Holiday Party
    """

    subgroup = models.ForeignKey(
        "subgroups.SubGroup",
        blank=True,
        null=True,
        help_text="Optional Sub-group (i.e. SIG)",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=64)
    default_title = models.CharField(max_length=64, null=True, blank=True)
    slug = models.SlugField(max_length=64, unique=True)
    description = tinymce_models.HTMLField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} | ({self.name})"

    class Meta:
        verbose_name = "Meeting Type"
        verbose_name_plural = "Meeting Types"


class Meeting(CommonModel):
    def __str__(self):
        if self.where:
            return f"{self.when:%a, %b %d %Y at %I:%M %p} at {self.where.name}"

        return f"{self.when} location TBD"

    when = models.DateTimeField()
    reg_close_date = models.DateTimeField("Registration Close Date", blank=True, null=True)
    where = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    # Used for anonymous access to meeting information like RSVPs
    key = models.CharField(max_length=40, unique=True, blank=True)
    live_stream = models.CharField(max_length=500, null=True, blank=True)
    meetup_id = models.TextField(blank=True, null=True)
    meeting_type = models.ForeignKey(
        MeetingType,
        blank=True,
        null=True,
        help_text=(
            "Type of meeting (i.e. SIG Meeting, "
            "Mentorship Meeting, Startup Row, etc.). "
            "Leave this empty for the main meeting. "
        ),
        on_delete=models.CASCADE,
    )
    custom_title = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text=(
            "If you fill out this field, this 'custom_title'"
            "will show up as the title of the event."
        ),
    )
    description = tinymce_models.HTMLField(blank=True, null=True)

    in_person_capacity = models.PositiveSmallIntegerField(null=False)
    virtual_capacity = models.PositiveSmallIntegerField(
        blank=True, null=True, help_text="Leave blank for no maximum"
    )

    def can_register(self):
        can_reg = True
        if self.reg_close_date and timezone.now() > self.reg_close_date:
            can_reg = False
        if timezone.now() > self.when:
            can_reg = False
        return can_reg

    def is_future(self):
        return bool(self.when >= (timezone.now() - datetime.timedelta(hours=3)))

    def rsvp_user_yes(self):
        raise NotImplementedError

    def number_rsvps(self):
        return self.rsvp_set.exclude(response=RSVP.Responses.DECLILNED).count()

    def number_in_person_rsvps(self):
        return self.rsvp_set.filter(
            response=RSVP.Responses.IN_PERSON,
            status=RSVP.Statuses.CONFIRMED,
        ).count()

    def number_virtual_rsvps(self):
        return self.rsvp_set.filter(
            response=RSVP.Responses.VIRTUAL,
            status=RSVP.Statuses.CONFIRMED,
        ).count()

    def is_in_person(self):
        return self.in_person_capacity != 0

    def is_virtual(self):
        return self.virtual_capacity != 0

    def has_in_person_capacity(self):

        max_capacity = self.in_person_capacity
        rsvps = self.rsvp_set.filter(
            response=RSVP.Responses.IN_PERSON,
            status=RSVP.Statuses.CONFIRMED,
        ).count()

        return max_capacity > rsvps

    def has_virtual_capacity(self):
        if self.virtual_capacity is None:
            return True

        max_capacity = self.virtual_capacity
        rsvps = self.rsvp_set.filter(
            response=RSVP.Responses.VIRTUAL,
            status=RSVP.Statuses.CONFIRMED,
        ).count()
        return max_capacity > rsvps

    def get_absolute_url(self):
        return reverse("meeting", args=[self.id])

    def meetup_url(self):
        return f"https://www.meetup.com/_ChiPy_/events/{self.meetup_id}/"

    @property
    def title(self):
        if self.custom_title:
            return self.custom_title
        if self.meeting_type and self.meeting_type.default_title:
            return self.meeting_type.default_title
        return "ChiPy __Main__ Meeting"  # quasi default title for the main meeting


class Presenter(CommonModel):
    def __str__(self):
        return f"{self.name} | ({self.email})"

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_LENGTH)
    email = models.EmailField(max_length=MAX_LENGTH, blank=True, null=True)
    phone = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    release = models.BooleanField(default=False)


LICENSE_CHOISES = (
    ("CC 0", "Creative Commons: No Rights Reserved"),
    ("CC BY", "Creative Commons: Attribution"),
    ("CC BY-SA", "Creative Commons: Attribution-ShareAlike"),
    ("CC BY-ND", "Creative Commons: Attribution-NoDerivs"),
    ("CC BY-NC", "Creative Commons: Attribution-NonCommercial"),
    ("CC BY-NC-SA", "Creative Commons: Attribution-NonCommercial-ShareAlike"),
    ("CC BY-NC-ND", "Creative Commons: Attribution-NonCommercial-NoDerivs"),
    ("All Rights Reserved", "All Rights Reserved"),
)

EXPERIENCE_LEVELS = (
    ("novice", "Novice"),
    ("intermediate", "Intermediate"),
    ("advanced", "Advanced"),
)


class TopicsQuerySet(models.QuerySet):
    def active(self):
        return self.filter(approved=True).order_by("start_time")


class Topic(CommonModel):
    def __str__(self):
        return self.title

    title = models.CharField(
        help_text="This will be the public title for your talk.", max_length=MAX_LENGTH
    )
    presenters = models.ManyToManyField(Presenter, blank=True)
    meeting = models.ForeignKey(
        Meeting,
        blank=True,
        null=True,
        related_name="topics",
        help_text=("Please select the meeting that you'd like to " "target your talk for."),
        on_delete=models.CASCADE,
    )
    experience_level = models.CharField(
        "Audience Experience Level",
        max_length=15,
        blank=True,
        null=True,
        choices=EXPERIENCE_LEVELS,
    )
    license = models.CharField(max_length=50, choices=LICENSE_CHOISES, default="CC BY")
    length = models.IntegerField(blank=True, null=True)
    embed_video = models.TextField(blank=True, null=True)
    description = tinymce_models.HTMLField(
        "Public Description",
        blank=True,
        null=True,
        help_text="This will be the public talk description.",
    )
    notes = models.TextField(
        "Private Submission Notes",
        blank=True,
        null=True,
        help_text=(
            "Additional non-public information or context "
            "you want us to know about the talk submission."
        ),
    )
    slides_link = models.URLField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    objects = TopicsQuerySet.as_manager()


class RSVP(CommonModel):
    class Responses:
        IN_PERSON = "in-person"
        VIRTUAL = "virtual"
        DECLILNED = "declined"
        ALL = [IN_PERSON, VIRTUAL, DECLILNED]
        CHOICE_LIST = [(IN_PERSON, "In-Person"), (VIRTUAL, "Virtually"), (DECLILNED, "Declined")]

    class Statuses:
        PENDING = "pending"
        CONFIRMED = "confirmed"
        WAIT_LISTED = "wait listed"
        REJECTED = "rejected"
        ALL = [PENDING, CONFIRMED, WAIT_LISTED, REJECTED]
        CHOICE_LIST = [
            (PENDING, "pending"),
            (CONFIRMED, "confirmed"),
            (REJECTED, "rejected"),
            (WAIT_LISTED, "wait listed"),
        ]

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    # willdo: remove name field keeping for migration purposes
    name = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)

    last_name = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    first_name = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    response = models.CharField(
        max_length=50, choices=Responses.CHOICE_LIST, default=Responses.IN_PERSON
    )
    status = models.CharField(max_length=50, choices=Statuses.CHOICE_LIST, default=Statuses.PENDING)

    key = models.CharField(max_length=MAX_LENGTH, blank=True, null=True)
    meetup_user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["-meeting", "last_name", "first_name"]
        verbose_name = "RSVP"

    def clean(self):
        if not self.user and not self.email:
            raise ValidationError("User or email required")

        # Check uniqueness
        if not self.id:
            if self.user:
                if RSVP.objects.filter(meeting=self.meeting, user=self.user).exists():
                    raise ValidationError("User has already RSVPed for meeting")
            else:
                if RSVP.objects.filter(meeting=self.meeting, email=self.email).exists():
                    raise ValidationError(
                        "A user with this email has already RSVPed for this meeting."
                    )

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        self.full_clean()

        original = None
        if self.id:
            original = RSVP.objects.get(id=self.id)

        # Generate a key for this RSVP
        if not self.key:
            self.key = "".join(
                random.choice(string.digits + string.ascii_lowercase) for x in range(40)
            )

        if not (original and original.response == self.response):
            if self.response == self.Responses.IN_PERSON:
                if self.meeting.has_in_person_capacity():
                    self.status = self.Statuses.CONFIRMED
                else:
                    self.status = self.Statuses.WAIT_LISTED

            if self.response == self.Responses.VIRTUAL:
                if self.meeting.has_virtual_capacity():
                    self.status = self.Statuses.CONFIRMED
                else:
                    self.status = self.Statuses.WAIT_LISTED

        if self.response == self.Responses.DECLILNED:
            self.status = self.Statuses.REJECTED

        return super().save(*args, **kwargs)

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return f"{self.meeting}: {self.full_name}"


@receiver(post_save, sender=RSVP)
def rsvp_post_save(sender, instance, **kwargs):

    # don't run on bulk or raw updates
    if kwargs["raw"]:
        return

    meeting: Meeting = instance.meeting

    # don't updated anything if registration is closed
    # if not meeting.can_register():
    #     return

    # send an email to the user by email
    if instance.email:
        send_rsvp_email(instance)

    if meeting.has_in_person_capacity():
        first_on_in_person_wait_list = (
            RSVP.objects.filter(
                meeting=meeting,
                response=RSVP.Responses.IN_PERSON,
                status=RSVP.Statuses.WAIT_LISTED,
            )
            .order_by("created")
            .first()
        )

        if first_on_in_person_wait_list:
            first_on_in_person_wait_list.status = RSVP.Statuses.CONFIRMED
            first_on_in_person_wait_list.save()

    if meeting.has_virtual_capacity():
        first_on_virtual_wait_list = (
            RSVP.objects.filter(
                meeting=meeting,
                response=RSVP.Responses.VIRTUAL,
                status=RSVP.Statuses.WAIT_LISTED,
            )
            .order_by("created")
            .first()
        )

        if first_on_virtual_wait_list:
            first_on_virtual_wait_list.status = RSVP.Statuses.CONFIRMED
            first_on_virtual_wait_list.save()
