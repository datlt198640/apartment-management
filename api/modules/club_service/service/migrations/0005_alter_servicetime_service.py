# Generated by Django 3.2.8 on 2022-01-05 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_alter_imageservice_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicetime',
            name='service',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='service_time', to='service.service'),
        ),
    ]