# Generated by Django 4.2.6 on 2024-02-04 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("companies", "0006_companies"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductMaterial",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(auto_now=True, db_index=True)),
                ("archived", models.DateTimeField(blank=True, null=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="price")),
                (
                    "material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="product_materials",
                        to="companies.stockmaterial",
                    ),
                ),
            ],
            options={
                "verbose_name": "product material",
                "verbose_name_plural": "product materials",
                "ordering": ("price",),
            },
        ),
    ]
