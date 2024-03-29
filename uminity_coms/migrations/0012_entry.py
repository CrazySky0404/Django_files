# Generated by Django 4.2.1 on 2023-07-07 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("uminity_coms", "0011_books"),
    ]

    operations = [
        migrations.CreateModel(
            name="Entry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("text", models.TextField(max_length=3000)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                (
                    "subtopic",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="uminity_coms.subtopic"),
                ),
            ],
        ),
    ]
