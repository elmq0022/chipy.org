# Generated by Django 3.2.10 on 2021-12-18 19:38

import chipy_org.libs.custom_ckeditor
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [
        ("meetings", "0001_squashed_0015_auto_20200208_1904"),
        ("meetings", "0002_auto_20200217_1825"),
        ("meetings", "0003_auto_20200629_0805"),
        ("meetings", "0004_add_cc0_license"),
        ("meetings", "0005_auto_20210110_1819"),
        ("meetings", "0005_auto_20201226_2020"),
        ("meetings", "0006_merge_20210214_1847"),
        ("meetings", "0007_auto_20211126_1905"),
        ("meetings", "0008_auto_20211213_1645"),
        ("meetings", "0009_alter_topic_description"),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("subgroups", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Presenter",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(blank=True, max_length=255, null=True)),
                ("phone", models.CharField(blank=True, max_length=255, null=True)),
                ("release", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Venue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(blank=True, max_length=255, null=True)),
                ("phone", models.CharField(blank=True, max_length=255, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                ("directions", models.TextField(blank=True, null=True)),
                ("embed_map", models.TextField(blank=True, null=True)),
                ("link", models.URLField(blank=True, null=True)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="MeetingType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=64)),
                ("slug", models.SlugField(max_length=64, unique=True)),
                ("description", ckeditor.fields.RichTextField(blank=True, null=True)),
                (
                    "subgroup",
                    models.ForeignKey(
                        blank=True,
                        help_text="Optional Sub-group (i.e. SIG)",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="subgroups.subgroup",
                    ),
                ),
                ("default_title", models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={"verbose_name": "Meeting Type", "verbose_name_plural": "Meeting Types",},
        ),
        migrations.CreateModel(
            name="Meeting",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("when", models.DateTimeField()),
                ("key", models.CharField(blank=True, max_length=40, unique=True)),
                ("live_stream", models.CharField(blank=True, max_length=500, null=True)),
                ("meetup_id", models.TextField(blank=True, null=True)),
                (
                    "where",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="meetings.venue",
                    ),
                ),
                ("description", ckeditor.fields.RichTextField(blank=True, null=True)),
                (
                    "meeting_type",
                    models.ForeignKey(
                        blank=True,
                        help_text="Type of meeting (i.e. SIG Meeting, Mentorship Meeting, Startup Row, etc.). Leave this empty for the main meeting. ",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="meetings.meetingtype",
                    ),
                ),
                (
                    "reg_close_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Registration Close Date"
                    ),
                ),
                (
                    "custom_title",
                    models.CharField(
                        blank=True,
                        help_text="If you fill out this field, this 'custom_title'will show up as the title of the event.",
                        max_length=64,
                        null=True,
                    ),
                ),
                ("in_person_capacity", models.PositiveSmallIntegerField(default=0)),
                (
                    "virtual_capacity",
                    models.PositiveSmallIntegerField(
                        blank=True, help_text="Leave blank for no maximum", null=True
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="RSVP",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("email", models.EmailField(blank=True, max_length=255, null=True)),
                (
                    "response",
                    models.CharField(
                        choices=[
                            ("in-person", "in-person"),
                            ("virtual", "virtual"),
                            ("declined", "declined"),
                        ],
                        default="in-person",
                        max_length=50,
                    ),
                ),
                ("key", models.CharField(blank=True, max_length=255, null=True)),
                ("meetup_user_id", models.IntegerField(blank=True, null=True)),
                (
                    "meeting",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="meetings.meeting"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=255, null=True)),
                ("last_name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "pending"),
                            ("confirmed", "confirmed"),
                            ("rejected", "rejected"),
                            ("wait listed", "wait listed"),
                        ],
                        default="pending",
                        max_length=50,
                    ),
                ),
            ],
            options={
                "abstract": False,
                "ordering": ["-meeting", "last_name", "first_name"],
                "verbose_name": "RSVP",
            },
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "title",
                    models.CharField(
                        help_text="This will be the public title for your talk.", max_length=255
                    ),
                ),
                (
                    "license",
                    models.CharField(
                        choices=[
                            ("CC 0", "Creative Commons: No Rights Reserved"),
                            ("CC BY", "Creative Commons: Attribution"),
                            ("CC BY-SA", "Creative Commons: Attribution-ShareAlike"),
                            ("CC BY-ND", "Creative Commons: Attribution-NoDerivs"),
                            ("CC BY-NC", "Creative Commons: Attribution-NonCommercial"),
                            (
                                "CC BY-NC-SA",
                                "Creative Commons: Attribution-NonCommercial-ShareAlike",
                            ),
                            ("CC BY-NC-ND", "Creative Commons: Attribution-NonCommercial-NoDerivs"),
                            ("All Rights Reserved", "All Rights Reserved"),
                        ],
                        default="CC BY",
                        max_length=50,
                    ),
                ),
                ("embed_video", models.TextField(blank=True, null=True)),
                (
                    "description",
                    chipy_org.libs.custom_ckeditor.CustomRichTextField(
                        blank=True, help_text="This will be the public talk description.", null=True
                    ),
                ),
                ("slides_link", models.URLField(blank=True, null=True)),
                ("start_time", models.DateTimeField(blank=True, null=True)),
                ("approved", models.BooleanField(default=False)),
                (
                    "meeting",
                    models.ForeignKey(
                        blank=True,
                        help_text="Please select the meeting that you'd like to target your talk for.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="topics",
                        to="meetings.meeting",
                    ),
                ),
                ("presenters", models.ManyToManyField(blank=True, to="meetings.Presenter")),
                (
                    "experience_level",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("novice", "Novice"),
                            ("intermediate", "Intermediate"),
                            ("advanced", "Advanced"),
                        ],
                        max_length=15,
                        null=True,
                        verbose_name="Audience Experience Level",
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        help_text="Additional non-public information or context you want us to know about the talk submission.",
                        null=True,
                        verbose_name="Private Submission Notes",
                    ),
                ),
                ("length", models.IntegerField(blank=True, null=True)),
            ],
            options={"abstract": False,},
        ),
    ]
