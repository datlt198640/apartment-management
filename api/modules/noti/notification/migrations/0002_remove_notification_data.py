# Generated by Django 3.2.8 on 2022-01-17 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='data',
        ),
    ]
