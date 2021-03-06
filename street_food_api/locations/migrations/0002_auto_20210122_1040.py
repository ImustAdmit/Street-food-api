# Generated by Django 3.1.5 on 2021-01-22 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="closed_at",
            field=models.TimeField(blank=True, verbose_name="Closed at"),
        ),
        migrations.AlterField(
            model_name="location",
            name="latitude",
            field=models.FloatField(blank=True, verbose_name="Latitude"),
        ),
        migrations.AlterField(
            model_name="location",
            name="longitude",
            field=models.FloatField(blank=True, verbose_name="Longitude"),
        ),
        migrations.AlterField(
            model_name="location",
            name="open_from",
            field=models.TimeField(blank=True, verbose_name="Open from"),
        ),
    ]
