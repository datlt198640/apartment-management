# Generated by Django 3.2.8 on 2022-01-20 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check_in', '0005_alter_checkin_check_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='is_check_out',
            field=models.BooleanField(default=False),
        ),
    ]
