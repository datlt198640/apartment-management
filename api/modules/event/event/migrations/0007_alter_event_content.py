# Generated by Django 3.2.8 on 2022-01-08 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_auto_20220108_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='content',
            field=models.TextField(blank=True, default=''),
        ),
    ]