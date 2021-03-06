# Generated by Django 2.1.2 on 2018-11-12 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0047_auto_20181112_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amendment',
            name='other_submitters',
        ),
        migrations.RemoveField(
            model_name='amendment',
            name='submitter',
        ),
        migrations.AddField(
            model_name='amendment',
            name='submitters',
            field=models.ManyToManyField(blank=True, related_name='submitters', through='parliament.AmendmentSubmitter', to='parliament.Member'),
        ),
        migrations.AddField(
            model_name='amendmentsubmitter',
            name='main',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='amendmentsubmitter',
            unique_together={('amendment', 'member'), ('amendment', 'main')},
        ),
    ]
