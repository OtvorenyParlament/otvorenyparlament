# Generated by Django 2.1.2 on 2018-11-09 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0040_auto_20181109_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='votingvote',
            name='voter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='parliament.Member'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='votingvote',
            unique_together={('voting', 'voter')},
        ),
    ]