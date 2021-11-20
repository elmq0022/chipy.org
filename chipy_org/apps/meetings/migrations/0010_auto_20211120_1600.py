# Generated by Django 2.2.17 on 2021-11-20 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0009_auto_20211120_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='in_person_capacity',
            field=models.PositiveSmallIntegerField(default=32767),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='meeting',
            name='virtual_capacity',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Leave blank for no maximum', null=True),
        ),
        migrations.AlterField(
            model_name='rsvp',
            name='venue',
            field=models.CharField(choices=[('I', 'In-Person'), ('V', 'Virtually')], default='I', max_length=1),
        ),
    ]