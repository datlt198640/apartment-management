# Generated by Django 3.2.8 on 2022-01-19 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0020_alter_bookingservice_deleted_at'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookingservice',
            unique_together=set(),
        ),
    ]
