# Generated by Django 3.2.8 on 2022-01-20 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0021_alter_bookingservice_unique_together'),
        ('notification', '0006_auto_20220119_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='membership_type',
        ),
        migrations.AddField(
            model_name='notification',
            name='member',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='member.member'),
        ),
    ]
