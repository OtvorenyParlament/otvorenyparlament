# Generated by Django 2.1.2 on 2018-10-11 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='external_id',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
