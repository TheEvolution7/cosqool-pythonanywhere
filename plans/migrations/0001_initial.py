# Generated by Django 4.2.4 on 2023-12-19 06:13

import ckeditor_uploader.fields
import core.models
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("courses", "0003_alter_category_image_alter_category_media_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Option",
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
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=core.models.upload_to,
                        verbose_name="image",
                    ),
                ),
                (
                    "media",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=core.models.upload_to,
                        verbose_name="media",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                ("status", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Option",
                "verbose_name_plural": "Options",
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="OptionTranslation",
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
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        blank=True,
                        max_length=255,
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "content",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True, verbose_name="content"
                    ),
                ),
                (
                    "position",
                    models.IntegerField(default=0, null=True, verbose_name="Position"),
                ),
            ],
            options={
                "verbose_name": "Option Translation",
                "db_table": "plans_option_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Plan",
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
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=core.models.upload_to,
                        verbose_name="image",
                    ),
                ),
                (
                    "media",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=core.models.upload_to,
                        verbose_name="media",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                ("status", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Plan",
                "verbose_name_plural": "Plans",
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="PlanItem",
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
                (
                    "paypal_plan_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("amount", models.FloatField(default=0.0)),
                ("currency", models.CharField(default="USD", max_length=10)),
                ("grades", models.ManyToManyField(blank=True, to="courses.grade")),
                (
                    "option",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plans.option",
                    ),
                ),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="plans.plan",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Price",
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
                ("currency", models.CharField(default="USD", max_length=3)),
                (
                    "price_amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
                ),
                (
                    "plan_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prices",
                        to="plans.planitem",
                    ),
                ),
            ],
            options={
                "verbose_name": "Price",
                "verbose_name_plural": "Prices",
            },
        ),
        migrations.CreateModel(
            name="PlanTranslation",
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
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        blank=True,
                        max_length=255,
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "content",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True, verbose_name="content"
                    ),
                ),
                (
                    "position",
                    models.IntegerField(default=0, null=True, verbose_name="Position"),
                ),
                (
                    "master",
                    parler.fields.TranslationsForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="plans.plan",
                    ),
                ),
            ],
            options={
                "verbose_name": "Plan Translation",
                "db_table": "plans_plan_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
