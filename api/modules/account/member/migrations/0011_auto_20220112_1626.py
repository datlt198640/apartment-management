# Generated by Django 3.2.8 on 2022-01-12 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0014_alter_service_subservice_type'),
        ('member', '0010_auto_20220111_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingservice',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='booking_service', to='member.member'),
        ),
        migrations.AlterUniqueTogether(
            name='bookingservice',
            unique_together={('service', 'member')},
        ),
    ]