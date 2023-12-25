# Generated by Django 4.2.1 on 2023-08-30 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("settings", "0005_remove_setting_image_picker_multiple_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="file",
            options={"verbose_name": "file", "verbose_name_plural": "files"},
        ),
        migrations.AddField(
            model_name="file",
            name="_file_size",
            field=models.BigIntegerField(
                blank=True, null=True, verbose_name="file size"
            ),
        ),
        migrations.AddField(
            model_name="file",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="description"),
        ),
        migrations.AddField(
            model_name="file",
            name="has_all_mandatory_data",
            field=models.BooleanField(
                default=False, editable=False, verbose_name="has all mandatory data"
            ),
        ),
        migrations.AddField(
            model_name="file",
            name="is_public",
            field=models.BooleanField(
                default=True,
                help_text="Disable any permission checking for this file. File will be publicly accessible to anyone.",
                verbose_name="Permissions disabled",
            ),
        ),
        migrations.AddField(
            model_name="file",
            name="mime_type",
            field=models.CharField(
                default="application/octet-stream",
                help_text="MIME type of uploaded content",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="file",
            name="modified_at",
            field=models.DateTimeField(auto_now=True, verbose_name="modified at"),
        ),
        migrations.AddField(
            model_name="file",
            name="name",
            field=models.CharField(
                blank=True, default="", max_length=255, verbose_name="name"
            ),
        ),
        migrations.AddField(
            model_name="file",
            name="original_filename",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="original filename"
            ),
        ),
        migrations.AddField(
            model_name="file",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="owned_%(class)ss",
                to=settings.AUTH_USER_MODEL,
                verbose_name="owner",
            ),
        ),
        migrations.AddField(
            model_name="file",
            name="sha1",
            field=models.CharField(
                blank=True, default="", max_length=40, verbose_name="sha1"
            ),
        ),
        migrations.AddField(
            model_name="file",
            name="uploaded_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="uploaded at",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="file",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="files/"),
        ),
    ]