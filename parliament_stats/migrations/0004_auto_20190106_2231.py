# Generated by Django 2.1.3 on 2019-01-06 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parliament_stats', '0003_auto_20181128_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalstats',
            name='bill_count_by_committee',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='globalstats',
            name='bill_count_by_government',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]