# Generated by Django 3.2.8 on 2022-01-09 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subservice', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subservicetype',
            name='service',
        ),
    ]
