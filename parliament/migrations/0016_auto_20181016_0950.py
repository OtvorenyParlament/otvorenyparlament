# Generated by Django 2.1.2 on 2018-10-16 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0015_auto_20181015_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='voting',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
