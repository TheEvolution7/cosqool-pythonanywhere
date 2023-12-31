# Generated by Django 4.2.1 on 2023-08-16 06:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("albums", "0010_alter_gallery_id_alter_group_id_alter_image_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="gallery",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name="group",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name="image",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
