# Generated by Django 2.1.2 on 2018-10-08 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0004_press_pressattachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('session_id', models.PositiveIntegerField()),
                ('session_num', models.PositiveIntegerField(blank=True, null=True)),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='parliament.Period')),
            ],
            options={
                'ordering': ('-period', '-session_num'),
            },
        ),
        migrations.CreateModel(
            name='SessionAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='missing title', max_length=512)),
                ('url', models.URLField()),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='parliament.Session')),
            ],
        ),
        migrations.CreateModel(
            name='SessionProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.PositiveIntegerField(blank=True, null=True)),
                ('state', models.CharField(max_length=128)),
                ('text', models.TextField(blank=True, null=True)),
                ('press', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='parliament.Press')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='points', to='parliament.Session')),
            ],
            options={
                'ordering': ('session', 'point'),
            },
        ),
    ]
