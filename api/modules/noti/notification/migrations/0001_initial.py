# Generated by Django 3.2.8 on 2022-01-17 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0019_device'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data', models.JSONField(blank=True, null=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('membership_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='member.membershiptype')),
            ],
            options={
                'db_table': 'notifications',
                'ordering': ['-id'],
            },
        ),
    ]
