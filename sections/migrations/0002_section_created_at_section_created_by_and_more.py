# Generated by Django 4.2.4 on 2023-12-13 04:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_initial"),
        ("sections", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="section",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="created at",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="section",
            name="created_by",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="section_created_by",
                to="accounts.teacher",
            ),
        ),
        migrations.AddField(
            model_name="section",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="updated at"),
        ),
        migrations.AddField(
            model_name="section",
            name="updated_by",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="section_updated_by",
                to="accounts.teacher",
            ),
        ),
    ]