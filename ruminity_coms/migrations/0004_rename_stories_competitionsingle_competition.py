# Generated by Django 4.0.6 on 2022-12-06 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ruminity_coms', '0003_alter_competition_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competitionsingle',
            old_name='stories',
            new_name='competition',
        ),
    ]
