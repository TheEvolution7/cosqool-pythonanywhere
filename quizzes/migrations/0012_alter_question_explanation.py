# Generated by Django 4.2.4 on 2024-01-02 09:34

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("quizzes", "0011_answer_image_alter_answer_question_alter_quiz_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="explanation",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                blank=True,
                help_text="Explanation to be shown after the question has been answered.",
                verbose_name="Explanation",
            ),
        ),
    ]
