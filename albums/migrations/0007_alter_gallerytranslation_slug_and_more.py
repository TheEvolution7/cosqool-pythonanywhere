# Generated by Django 4.2.1 on 2023-07-25 05:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("albums", "0006_alter_group_parent_alter_image_gallery"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gallerytranslation",
            name="slug",
            field=models.SlugField(
                allow_unicode=True,
                blank=True,
                max_length=255,
                unique=True,
                verbose_name="slug",
            ),
        ),
        migrations.AlterField(
            model_name="grouptranslation",
            name="slug",
            field=models.SlugField(
                allow_unicode=True,
                blank=True,
                max_length=255,
                unique=True,
                verbose_name="slug",
            ),
        ),
        migrations.AlterField(
            model_name="imagetranslation",
            name="slug",
            field=models.SlugField(
                allow_unicode=True,
                blank=True,
                max_length=255,
                unique=True,
                verbose_name="slug",
            ),
        ),
    ]
