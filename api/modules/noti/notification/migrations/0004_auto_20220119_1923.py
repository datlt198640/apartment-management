# Generated by Django 3.2.8 on 2022-01-19 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_alter_notification_membership_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='notification',
            name='title',
            field=models.TextField(),
        ),
    ]
