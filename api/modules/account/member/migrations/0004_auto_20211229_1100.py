# Generated by Django 3.2.8 on 2021-12-29 11:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_rename_fullname_member_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='expire_date',
        ),
        migrations.RemoveField(
            model_name='member',
            name='register_date',
        ),
        migrations.RemoveField(
            model_name='member',
            name='type',
        ),
        migrations.CreateModel(
            name='MemberShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.IntegerField(choices=[(0, 'None'), (1, 'Member'), (2, 'Wellness member')])),
                ('register_date', models.DateField(default=datetime.datetime.today)),
                ('expire_date', models.DateField(default=datetime.datetime.today)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='member.member')),
            ],
            options={
                'db_table': 'memberships',
                'ordering': ['-id'],
            },
        ),
    ]
