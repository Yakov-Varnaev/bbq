# Generated by Django 4.2.6 on 2023-12-14 08:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_add_user_model"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="bio",
            field=models.TextField(default="", max_length=250, verbose_name="bio"),
            preserve_default=False,
        ),
    ]
