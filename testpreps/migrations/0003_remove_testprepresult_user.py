# Generated by Django 4.2.4 on 2023-12-19 07:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("testpreps", "0002_alter_testprepitemresult_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="testprepresult",
            name="user",
        ),
    ]
