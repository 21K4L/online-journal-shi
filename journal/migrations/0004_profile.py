# Generated by Django 5.1.5 on 2025-01-21 11:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0003_remove_article_is_recent"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bio", models.TextField(blank=True, max_length=100)),
                (
                    "prof_picture",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_pictures/"
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=100)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
