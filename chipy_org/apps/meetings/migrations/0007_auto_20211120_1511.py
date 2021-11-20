# Generated by Django 2.2.17 on 2021-11-20 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0006_merge_20210214_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='rsvp',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('D', 'Declined'), ('W', 'Wait Listed')], default='A', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rsvp',
            name='venue',
            field=models.CharField(choices=[('I', 'In Person'), ('V', 'Virtual')], default='V', max_length=1),
            preserve_default=False,
        ),
    ]