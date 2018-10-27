# Generated by Django 2.1.2 on 2018-10-27 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parliament', '0026_auto_20181027_1327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clubmember',
            options={'ordering': ('club', 'member', 'start')},
        ),
        migrations.AlterModelOptions(
            name='memberactive',
            options={'ordering': ('member', 'start')},
        ),
        migrations.AlterField(
            model_name='clubmember',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='parliament.Club'),
        ),
    ]