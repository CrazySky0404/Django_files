# Generated by Django 4.2.1 on 2023-07-09 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("uminity_coms", "0014_delete_blockbook_alter_subtopic_date_added"),
    ]

    operations = [
        migrations.AddField(
            model_name="subtopic",
            name="comment_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="subtopic",
            name="date_added",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
