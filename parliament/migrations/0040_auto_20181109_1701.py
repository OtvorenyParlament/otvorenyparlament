# Generated by Django 2.1.2 on 2018-11-09 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0039_auto_20181109_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debateappearance',
            name='debater',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='parliament.Member'),
        ),
    ]
