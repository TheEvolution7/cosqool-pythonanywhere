# Generated by Django 4.2.1 on 2023-09-11 03:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("settings", "0007_setting_image_picker_multiple"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="setting",
            name="image_picker",
        ),
        migrations.RemoveField(
            model_name="setting",
            name="image_picker_multiple",
        ),
        migrations.DeleteModel(
            name="File",
        ),
    ]