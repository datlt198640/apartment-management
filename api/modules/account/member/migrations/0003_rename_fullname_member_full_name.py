# Generated by Django 3.2.8 on 2021-12-27 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20211227_1129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='fullname',
            new_name='full_name',
        ),
    ]
