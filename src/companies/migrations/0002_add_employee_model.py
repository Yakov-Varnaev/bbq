# Generated by Django 4.2.6 on 2023-10-14 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "departments",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="employees", to="companies.department"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="employees",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "employee",
                "verbose_name_plural": "employees",
                "unique_together": {("departments", "user")},
            },
        ),
    ]
