# Generated by Django 3.2.8 on 2022-07-15 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0032_member_member_remote_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='member_remote_id',
        ),
    ]
