# Generated by Django 5.1.5 on 2025-01-24 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("journal", "0007_remove_profile_role_userprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="comment",
            field=models.TextField(blank=True, null=True),
        ),
    ]
