# Generated by Django 5.1.2 on 2024-12-23 12:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthapp', '0004_healthrecord_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('walk_minutes', models.PositiveIntegerField(default=0)),
                ('playtime_minutes', models.PositiveIntegerField(default=0)),
                ('mental_stimulation_minutes', models.PositiveIntegerField(default=0)),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='healthapp.dogprofile')),
            ],
        ),
    ]
