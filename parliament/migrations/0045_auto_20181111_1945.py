# Generated by Django 2.1.2 on 2018-11-11 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0044_amendment_title'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='billproposer',
            unique_together={('bill', 'member')},
        ),
    ]
