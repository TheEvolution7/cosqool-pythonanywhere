# Generated by Django 4.2.4 on 2023-12-08 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("lessons", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Sitting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "question_order",
                    models.CharField(max_length=1024, verbose_name="Question Order"),
                ),
                (
                    "question_list",
                    models.CharField(max_length=1024, verbose_name="Question List"),
                ),
                (
                    "incorrect_questions",
                    models.CharField(
                        blank=True, max_length=1024, verbose_name="Incorrect questions"
                    ),
                ),
                ("current_score", models.IntegerField(verbose_name="Current Score")),
                (
                    "complete",
                    models.BooleanField(default=False, verbose_name="Complete"),
                ),
                (
                    "user_answers",
                    models.JSONField(
                        blank=True, null=True, verbose_name="User Answers"
                    ),
                ),
                (
                    "start",
                    models.DateTimeField(auto_now_add=True, verbose_name="Start"),
                ),
                (
                    "end",
                    models.DateTimeField(blank=True, null=True, verbose_name="End"),
                ),
                (
                    "test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lessons.test",
                        verbose_name="Test",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "permissions": (("view_sittings", "Can see completed exams."),),
            },
        ),
        migrations.CreateModel(
            name="Progress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.CharField(max_length=1024, verbose_name="Score")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "User Progress",
                "verbose_name_plural": "User progress records",
            },
        ),
    ]
