# Generated by Django 3.2.8 on 2022-01-07 17:02

from django.db import migrations, models
import modules.account.member.models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_auto_20220107_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=modules.account.member.models.upload_avatar),
        ),
    ]
