# Generated by Django 3.2.8 on 2022-01-07 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_service_has_menu'),
        ('member', '0007_member_qr_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('status', models.IntegerField(choices=[(0, 'NONE '), (1, 'READY ')])),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_service', to='member.member')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_service', to='service.service')),
            ],
            options={
                'db_table': 'booking_services',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='member',
            name='services',
            field=models.ManyToManyField(related_name='members', through='member.BookingService', to='service.Service'),
        ),
    ]
