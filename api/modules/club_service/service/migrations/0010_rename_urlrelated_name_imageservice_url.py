# Generated by Django 3.2.8 on 2022-01-08 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0009_auto_20220108_2128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imageservice',
            old_name='urlrelated_name',
            new_name='url',
        ),
    ]
