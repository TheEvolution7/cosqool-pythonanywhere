# Generated by Django 4.2.4 on 2023-12-19 08:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("testpreps", "0005_alter_testprepitemresult_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="testprepitemresult",
            name="status",
            field=models.CharField(
                choices=[
                    ("in-process", "In Process"),
                    ("completed", "Completed"),
                    ("cancelled", "Cancelled"),
                ],
                default="in-process",
                max_length=14,
            ),
        ),
    ]
