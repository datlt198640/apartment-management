# Generated by Django 3.2.8 on 2022-01-20 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0022_auto_20220120_1523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notificationmember',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelTable(
            name='notificationmember',
            table='notification_members',
        ),
    ]