# Generated by Django 4.1 on 2023-04-03 07:51

import contacts.models
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0009_alter_group_options_alter_grouptranslation_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=contacts.models.user_directory_path, verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='note',
            field=models.TextField(blank=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, db_index=True, default='', max_length=128, region=None, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='grouptranslation',
            name='description',
            field=models.TextField(blank=True, default=1, verbose_name='description'),
            preserve_default=False,
        ),
    ]
