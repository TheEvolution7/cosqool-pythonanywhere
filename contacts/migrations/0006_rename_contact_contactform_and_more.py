# Generated by Django 4.1 on 2023-04-02 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_alter_messagetranslation_mail_sent_ng_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contact',
            new_name='ContactForm',
        ),
        migrations.RenameModel(
            old_name='ContactTranslation',
            new_name='ContactFormTranslation',
        ),
        migrations.AlterModelOptions(
            name='contactform',
            options={'verbose_name': 'Contact Form', 'verbose_name_plural': 'Contact Forms'},
        ),
        migrations.AlterModelOptions(
            name='contactformtranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Contact Form Translation'},
        ),
        migrations.RenameField(
            model_name='mail',
            old_name='contact',
            new_name='contact_form',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='contact',
            new_name='contact_form',
        ),
        migrations.AlterModelTable(
            name='contactformtranslation',
            table='contacts_contactform_translation',
        ),
    ]
