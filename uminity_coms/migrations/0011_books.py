# Generated by Django 4.2.1 on 2023-07-02 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("uminity_coms", "0010_alter_competitionsingle_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="Books",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.CharField(max_length=300)),
                ("description", models.TextField(null=True)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
