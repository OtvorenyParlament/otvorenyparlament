# Generated by Django 2.1.2 on 2018-11-09 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0042_remove_votingvote_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='interpellation',
            name='interpellation_session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interpellations', to='parliament.Session'),
        ),
        migrations.AddField(
            model_name='interpellation',
            name='press',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='parliament.Press'),
        ),
        migrations.AddField(
            model_name='interpellation',
            name='response_session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interpellation_responses', to='parliament.Session'),
        ),
    ]
