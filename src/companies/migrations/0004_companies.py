# Generated by Django 4.2.6 on 2024-01-15 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0003_default_ordering_for_stock_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="Procedure",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="procedure name")),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="procedures",
                        to="companies.department",
                        verbose_name="department",
                    ),
                ),
                (
                    "kind",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="procedures",
                        to="companies.materialtype",
                        verbose_name="material type",
                    ),
                ),
            ],
            options={
                "verbose_name": "procedure",
                "verbose_name_plural": "procedures",
                "ordering": ("name",),
            },
        ),
    ]
