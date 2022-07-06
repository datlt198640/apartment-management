# Generated by Django 3.2.8 on 2021-12-28 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service', '0002_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubserviceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=225, unique=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subservice_type', to='service.service')),
            ],
            options={
                'db_table': 'subservice_types',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SubserviceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=225, unique=True)),
                ('description', models.CharField(blank=True, default='', max_length=225)),
                ('content', models.TextField()),
                ('subservice_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subservice_category', to='subservice.subservicetype')),
            ],
            options={
                'db_table': 'subservice_categories',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Subservice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225, unique=True)),
                ('description', models.CharField(blank=True, default='', max_length=225)),
                ('content', models.TextField()),
                ('price', models.FloatField(default=0.0)),
                ('open_time', models.TimeField(null=True)),
                ('duration', models.IntegerField(null=True)),
                ('subservice_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subservice', to='subservice.subservicecategory')),
            ],
            options={
                'db_table': 'subservices',
                'ordering': ['-id'],
            },
        ),
    ]