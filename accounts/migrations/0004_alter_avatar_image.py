# Generated by Django 4.2.4 on 2023-12-13 10:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_parent_language_alter_student_language_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avatar",
            name="image",
            field=models.ImageField(upload_to="avatars"),
        ),
    ]
