# Generated by Django 2.2.17 on 2021-11-24 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0012_auto_20211123_0601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rsvp',
            name='attendance_type',
        ),
        migrations.AlterField(
            model_name='rsvp',
            name='response',
            field=models.CharField(choices=[('in-person', 'In-Person'), ('virtual', 'Virtually'), ('declined', 'Declined')], default='in-person', max_length=50),
        ),
        migrations.AlterField(
            model_name='rsvp',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('confirmed', 'confirimed'), ('rejected', 'rejected'), ('wait listed', 'wait listed')], default='pending', max_length=50),
        ),
    ]