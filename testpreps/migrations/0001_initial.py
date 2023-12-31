# Generated by Django 4.2.4 on 2023-12-19 06:13

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("quizzes", "0010_alter_question_quiz"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("courses", "0003_alter_category_image_alter_category_media_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0004_alter_avatar_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Part",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "position",
                    models.IntegerField(default=0, null=True, verbose_name="Position"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                ("status", models.BooleanField(default=True)),
                (
                    "max_questions",
                    models.PositiveIntegerField(
                        default=1,
                        help_text="Number of questions to be answered on each attempt.",
                        verbose_name="Max Questions",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to="accounts.student",
                    ),
                ),
                (
                    "questions",
                    models.ManyToManyField(blank=True, to="quizzes.question"),
                ),
                ("quizzes", models.ManyToManyField(blank=True, to="quizzes.quiz")),
                (
                    "updated_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_updated_by",
                        to="accounts.student",
                    ),
                ),
            ],
            options={
                "verbose_name": "Part",
                "verbose_name_plural": "Parts",
            },
        ),
        migrations.CreateModel(
            name="TestPrep",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("status", models.BooleanField(default=True)),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "slug",
                    models.SlugField(
                        allow_unicode=True,
                        blank=True,
                        max_length=255,
                        unique=True,
                        verbose_name="slug",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "content",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True, verbose_name="content"
                    ),
                ),
                (
                    "position",
                    models.IntegerField(default=0, null=True, verbose_name="Position"),
                ),
                (
                    "course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="testpreps",
                        to="courses.course",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to="accounts.student",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_updated_by",
                        to="accounts.student",
                    ),
                ),
            ],
            options={
                "verbose_name": "TestPrep",
                "verbose_name_plural": "TestPreps",
            },
        ),
        migrations.CreateModel(
            name="TestPrepItem",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "position",
                    models.IntegerField(default=0, null=True, verbose_name="Position"),
                ),
                ("status", models.BooleanField(default=True)),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                ("time", models.DurationField(default=0)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to="accounts.student",
                    ),
                ),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_%(app_label)s.%(class)s_set+",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "testprep",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="testpreps.testprep",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_updated_by",
                        to="accounts.student",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
        ),
        migrations.CreateModel(
            name="TestprepItemResult",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "position",
                    models.IntegerField(default=0, null=True, verbose_name="Position"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                ("total_score", models.PositiveIntegerField(default=0)),
                ("results", models.JSONField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("scored", "Scored"),
                            ("released", "Released"),
                            ("cancelled", "Cancelled"),
                            ("pending_review", "Pending Review"),
                        ],
                        default="pending",
                        max_length=14,
                    ),
                ),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to="accounts.student",
                    ),
                ),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_%(app_label)s.%(class)s_set+",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "testprep_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_testprep_item",
                        to="testpreps.testprepitem",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
        ),
        migrations.CreateModel(
            name="Breake",
            fields=[
                (
                    "testprepitem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="testpreps.testprepitem",
                    ),
                ),
            ],
            options={
                "verbose_name": "Breake",
                "verbose_name_plural": "Breakes",
            },
            bases=("testpreps.testprepitem",),
        ),
        migrations.CreateModel(
            name="BreakeResult",
            fields=[
                (
                    "testprepitemresult_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="testpreps.testprepitemresult",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("testpreps.testprepitemresult",),
        ),
        migrations.CreateModel(
            name="SectionResult",
            fields=[
                (
                    "testprepitemresult_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="testpreps.testprepitemresult",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            bases=("testpreps.testprepitemresult",),
        ),
        migrations.CreateModel(
            name="TestprepResult",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "position",
                    models.IntegerField(default=0, null=True, verbose_name="Position"),
                ),
                ("total_score", models.PositiveIntegerField(default=0)),
                ("results", models.JSONField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("scored", "Scored"),
                            ("released", "Released"),
                            ("cancelled", "Cancelled"),
                            ("pending_review", "Pending Review"),
                        ],
                        default="pending",
                        max_length=14,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to="accounts.student",
                    ),
                ),
                (
                    "testprep",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="testprep_results",
                        to="testpreps.testprep",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_updated_by",
                        to="accounts.student",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Testprep Result",
                "verbose_name_plural": "Testprep Results",
            },
        ),
        migrations.AddField(
            model_name="testprepitemresult",
            name="testprep_result",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_testprep_result",
                to="testpreps.testprepresult",
            ),
        ),
        migrations.AddField(
            model_name="testprepitemresult",
            name="updated_by",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_updated_by",
                to="accounts.student",
            ),
        ),
        migrations.CreateModel(
            name="Bookmark",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "position",
                    models.IntegerField(default=0, null=True, verbose_name="Position"),
                ),
                ("status", models.BooleanField(default=True)),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to="accounts.student",
                    ),
                ),
                (
                    "part",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmark_parts",
                        to="testpreps.part",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmark_questions",
                        to="quizzes.question",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_updated_by",
                        to="accounts.student",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookmark_users",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "testprepitem_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="testpreps.testprepitem",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
            ],
            options={
                "verbose_name": "Section",
                "verbose_name_plural": "Sections",
                "order_with_respect_to": "testprep",
            },
            bases=("testpreps.testprepitem",),
        ),
        migrations.CreateModel(
            name="PartResult",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "position",
                    models.IntegerField(default=0, null=True, verbose_name="Position"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                ("content", models.JSONField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("scored", "Scored"),
                            ("released", "Released"),
                            ("cancelled", "Cancelled"),
                            ("completed", "Completed"),
                        ],
                        default="pending",
                        max_length=14,
                    ),
                ),
                ("question_random_list", models.JSONField(blank=True, null=True)),
                ("user_answers", models.JSONField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_created_by",
                        to="accounts.student",
                    ),
                ),
                (
                    "part",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="part_partresults",
                        to="testpreps.part",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_updated_by",
                        to="accounts.student",
                    ),
                ),
                (
                    "section_result",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="testprepresult_partresults",
                        to="testpreps.sectionresult",
                    ),
                ),
            ],
            options={
                "verbose_name": "Part Result",
                "verbose_name_plural": "Part Results",
            },
        ),
        migrations.AddField(
            model_name="part",
            name="section",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="parts",
                to="testpreps.section",
            ),
        ),
        migrations.AlterOrderWithRespectTo(
            name="part",
            order_with_respect_to="section",
        ),
    ]
