# Generated by Django 3.2.8 on 2022-01-10 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subservice', '0002_remove_subservicetype_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='subservicetype',
            name='uid',
            field=models.CharField(default=None, max_length=225, null=True, unique=True),
        ),
    ]
