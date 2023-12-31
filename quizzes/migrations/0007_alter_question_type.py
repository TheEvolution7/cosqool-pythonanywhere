# Generated by Django 4.2.4 on 2023-12-08 09:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quizzes", "0006_question_explanation_question_figure"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="type",
            field=models.CharField(
                choices=[
                    (
                        "Multiple Choice Questions",
                        (
                            ("single_select", "Single Select"),
                            ("multi_select", "Multi-Select"),
                            ("dropdown", "Dropdown Menu"),
                            ("star_rating", "Star Rating"),
                            ("text_slider", "Text Slider"),
                            ("numeric_slider", "Numeric Slider"),
                            ("thumbs_up_down", "Thumbs Up/Down"),
                            ("matrix_table", "Matrix Table"),
                            ("rank_order", "Rank Order"),
                            ("image_based", "Image/Picture Based"),
                        ),
                    ),
                    ("TF", "True/False"),
                    ("SHORT", "Short Answer"),
                    ("ESSAY", "Essay"),
                ],
                default="Multiple Choice Questions",
                max_length=14,
            ),
        ),
    ]
