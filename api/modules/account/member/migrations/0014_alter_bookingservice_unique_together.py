# Generated by Django 3.2.8 on 2022-01-13 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0013_remove_bookingservice_status'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookingservice',
            unique_together=set(),
        ),
    ]