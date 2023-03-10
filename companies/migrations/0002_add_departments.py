# Generated by Django 4.1.6 on 2023-02-14 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=255)),
                (
                    'point',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='departments',
                        to='companies.companypoint',
                    ),
                ),
            ],
        ),
    ]
