# Generated by Django 3.2.8 on 2022-01-12 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0011_auto_20220112_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingservice',
            name='member',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_service', to='member.member'),
        ),
    ]