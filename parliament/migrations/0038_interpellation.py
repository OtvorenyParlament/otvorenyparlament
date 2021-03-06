# Generated by Django 2.1.2 on 2018-11-09 15:30

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0003_remove_person_external_url'),
        ('parliament', '0037_debateappearance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interpellation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.PositiveIntegerField(unique=True)),
                ('date', models.DateField()),
                ('status', models.SmallIntegerField(choices=[(0, 'Príjem odpovede na interpeláciu'), (1, 'Rokovanie o interpelácii'), (2, 'Uzavretá odpoveď na interpeláciu')])),
                ('responded_by', models.CharField(blank=True, default='', max_length=64)),
                ('recipients', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), size=None)),
                ('url', models.URLField()),
                ('description', models.TextField()),
                ('asked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='person.Person')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parliament.Period')),
            ],
        ),
    ]
