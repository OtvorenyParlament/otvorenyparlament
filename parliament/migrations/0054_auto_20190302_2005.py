# Generated by Django 2.1.3 on 2019-03-02 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0053_auto_20190113_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interpellation',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Príjem odpovede na interpeláciu'), (1, 'Rokovanie o interpelácii'), (2, 'Uzavretá odpoveď na interpeláciu'), (3, 'Interpelácia na expedíciu')]),
        ),
    ]
