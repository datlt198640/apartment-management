# Generated by Django 3.2.8 on 2021-12-20 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=64, unique=True)),
                ('value', models.CharField(blank=True, default='', max_length=255)),
            ],
            options={
                'db_table': 'variables',
                'ordering': ['-id'],
            },
        ),
    ]
