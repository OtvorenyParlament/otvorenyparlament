# Generated by Django 2.1.2 on 2018-10-27 11:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0025_auto_20181019_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='external_id',
            field=models.IntegerField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='club',
            name='url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='clubmember',
            name='membership',
            field=models.CharField(choices=[('', 'Žiadny'), ('chairman', 'Predsedníčka/predseda'), ('vice-chairman', 'Pod-predsedníčka/predseda'), ('member', 'Členka/člen')], db_index=True, default='', max_length=24),
        ),
        migrations.AlterField(
            model_name='clubmember',
            name='start',
            field=models.DateField(default=datetime.datetime(1990, 1, 1, 0, 0)),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='club',
            unique_together={('period', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='clubmember',
            unique_together={('club', 'member', 'start')},
        ),
    ]