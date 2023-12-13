# Generated by Django 4.2.4 on 2023-12-08 09:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("fields", "0004_alter_field_status_alter_group_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="field",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name="group",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
