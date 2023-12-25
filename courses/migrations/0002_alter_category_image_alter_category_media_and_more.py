# Generated by Django 4.2.4 on 2023-12-13 10:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="%(class)s/", verbose_name="image"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="media",
            field=models.FileField(
                blank=True, null=True, upload_to="%(class)s/", verbose_name="media"
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="%(class)s/", verbose_name="image"
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="media",
            field=models.FileField(
                blank=True, null=True, upload_to="%(class)s/", verbose_name="media"
            ),
        ),
        migrations.AlterField(
            model_name="grade",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="%(class)s/", verbose_name="image"
            ),
        ),
        migrations.AlterField(
            model_name="grade",
            name="media",
            field=models.FileField(
                blank=True, null=True, upload_to="%(class)s/", verbose_name="media"
            ),
        ),
        migrations.AlterField(
            model_name="subject",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="%(class)s/", verbose_name="image"
            ),
        ),
        migrations.AlterField(
            model_name="subject",
            name="media",
            field=models.FileField(
                blank=True, null=True, upload_to="%(class)s/", verbose_name="media"
            ),
        ),
    ]