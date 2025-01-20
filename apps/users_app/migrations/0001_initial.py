# Generated by Django 5.1.5 on 2025-01-20 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('address', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
            },
        ),
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('tg_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, null=True)),
                ('fullname', models.CharField(max_length=255, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('chat_lang', models.CharField(choices=[('uz', 'Uzbek'), ('ru', 'Russian'), ('en', 'English')], max_length=2)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users_app.location')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['-registered_at'],
            },
        ),
    ]
