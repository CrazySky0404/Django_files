# Generated by Django 4.0.6 on 2022-08-24 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruminity_coms', '0004_entry_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='description',
        ),
        migrations.AddField(
            model_name='topic',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
