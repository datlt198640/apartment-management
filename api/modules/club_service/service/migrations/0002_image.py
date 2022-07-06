# Generated by Django 3.2.8 on 2021-12-28 18:54

from django.db import migrations, models
import django.db.models.deletion
import modules.club_service.service.models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('url', models.ImageField(blank=True, null=True, upload_to=modules.club_service.service.models.upload_to)),
                ('title', models.CharField(max_length=225)),
                ('description', models.CharField(max_length=225)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='service.service')),
            ],
            options={
                'db_table': 'images',
                'ordering': ['-id'],
            },
        ),
    ]
