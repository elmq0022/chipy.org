# Generated by Django 5.1.3 on 2024-11-23 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("announcements", "0001_initial_squashed_0005_remove_announcement_text"),
    ]

    operations = [
        migrations.RenameField(
            model_name="announcement",
            old_name="text2",
            new_name="text",
        ),
    ]