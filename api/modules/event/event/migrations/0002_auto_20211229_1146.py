# Generated by Django 3.2.8 on 2021-12-29 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_auto_20211229_1100'),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='end_date',
            new_name='end_time',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='start_date',
            new_name='start_time',
        ),
        migrations.CreateModel(
            name='EventMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_member', to='event.event')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_member', to='member.member')),
            ],
            options={
                'db_table': 'event_members',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='event',
            name='member',
            field=models.ManyToManyField(through='event.EventMember', to='member.Member'),
        ),
    ]