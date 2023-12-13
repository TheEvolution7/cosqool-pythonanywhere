# Generated by Django 4.2.1 on 2023-08-16 06:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("albums", "0012_alter_gallery_uuid_alter_group_uuid_alter_image_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gallery",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name="group",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name="image",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
