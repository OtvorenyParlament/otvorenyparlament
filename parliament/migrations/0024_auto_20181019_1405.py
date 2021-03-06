# Generated by Django 2.1.2 on 2018-10-19 12:05

from datetime import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0023_auto_20181018_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='period',
            name='year_end',
        ),
        migrations.RemoveField(
            model_name='period',
            name='year_start',
        ),
        migrations.AddField(
            model_name='period',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='period',
            name='start_date',
            field=models.DateField(default=datetime(2016, 1, 1).date),
            preserve_default=False,
        ),
    ]
