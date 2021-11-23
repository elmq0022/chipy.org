# Generated by Django 2.2.17 on 2021-11-20 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0010_auto_20211120_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rsvp',
            name='status',
            field=models.CharField(blank=True, choices=[('A', 'Accepted'), ('D', 'Declined'), ('W', 'Wait Listed')], max_length=1, null=True),
        ),
    ]