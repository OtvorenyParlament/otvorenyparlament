# Generated by Django 2.1.2 on 2018-10-17 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0021_auto_20181017_1025'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='clubmember',
            unique_together={('club', 'member', 'membership')},
        ),
    ]
