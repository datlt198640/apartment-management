# Generated by Django 3.2.8 on 2022-01-17 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_eventmember_noti_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventmember',
            name='noti_status',
        ),
    ]
