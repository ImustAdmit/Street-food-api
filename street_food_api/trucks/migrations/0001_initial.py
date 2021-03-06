# Generated by Django 3.1.5 on 2021-01-19 17:13

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models

import conf.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentMethod",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "payment_name",
                    models.CharField(
                        max_length=30, verbose_name="Payment Name"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Truck",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Name")),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        max_length=50,
                        region=None,
                        verbose_name="Phone",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=50, verbose_name="Email"
                    ),
                ),
                (
                    "facebook",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Facebook"
                    ),
                ),
                (
                    "instagram",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Instagram"
                    ),
                ),
                (
                    "page_url",
                    models.URLField(blank=True, verbose_name="Page URL"),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=200, verbose_name="Description"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created"
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Updated"
                    ),
                ),
                ("slug", models.SlugField(editable=False)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trucks",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Owner",
                    ),
                ),
                (
                    "payment_methods",
                    models.ManyToManyField(
                        related_name="payments",
                        to="trucks.PaymentMethod",
                        verbose_name="Payment Methods",
                    ),
                ),
            ],
            options={
                "verbose_name": "Truck",
                "verbose_name_plural": "Trucks",
            },
        ),
        migrations.CreateModel(
            name="TruckImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to=conf.utils.image_directory_path,
                        verbose_name="Image",
                    ),
                ),
                (
                    "truck",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="trucks.truck",
                        verbose_name="Truck",
                    ),
                ),
            ],
            options={
                "verbose_name": "Image",
                "verbose_name_plural": "Images",
            },
        ),
    ]
