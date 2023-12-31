# Generated by Django 4.2.4 on 2023-12-13 06:47

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articlecategory",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="articles.articlecategory",
            ),
        ),
    ]
