# Generated by Django 5.1.5 on 2025-01-20 11:28

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_attempts', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_app.botuser')),
            ],
            options={
                'verbose_name': 'Result',
                'verbose_name_plural': 'Results',
                'ordering': ['number_of_attempts'],
            },
        ),
    ]
