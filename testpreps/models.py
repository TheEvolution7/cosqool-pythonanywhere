from sqlite3 import complete_statement
from accounts.models import *
from django.db import models
from django.utils.translation import gettext_lazy as _
from courses.models import Course

from django.db.models import Sum, Count
from quizzes.models import Question, Quiz
import random
import uuid
from polymorphic.models import PolymorphicModel
from ckeditor_uploader.fields import RichTextUploadingField


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    position = models.IntegerField(_("Position"), null=True, default=0)
    status = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
        default=1,
    )
    updated_by = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="%(class)s_updated_by",
        default=1,
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]


class TestPrep(BaseModel):
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(
        _("slug"), unique=True, blank=True, max_length=255, allow_unicode=True
    )

    description = models.TextField(_("description"), null=True, blank=True)
    content = RichTextUploadingField(_("content"), null=True, blank=True)
    position = models.IntegerField(_("Position"), null=True, default=0)

    course = models.ForeignKey(
        Course, models.CASCADE, null=True, blank=True, related_name="testpreps"
    )
    time = models.DurationField(default=0)

    class Meta:
        verbose_name = _("Test Prep")
        verbose_name_plural = _("Test Preps")

    def get_items(self):
        return self.items.filter(status=True).order_by("position")

    def get_sections(self):
        return self.items.instance_of(Section).filter(status=True).all()

    def get_total_questions(self):
        return self.get_parts().aggregate(Count("questions"))["questions__count"]

    def get_total_time(self):
        return self.items.aggregate(Sum("time"))["time__sum"]

    def get_total_duration_parts(self):
        return self.get_parts().aggregate(total_duration_part=Sum("time"))[
            "total_duration_part"
        ]

    def get_total_score_part(self):
        return self.get_parts().aggregate(Count("questions"))["questions__count"]

    def get_total_score_part_result(self):
        return (
            self.testprep_results.filter().aggregate(total_score=Sum("score"))[
                "total_score"
            ]
            or 0
        )

    def get_testprep_results_by_user(self):
        return self.testprep_results.filter().all()

    class Meta:
        verbose_name = _("TestPrep")
        verbose_name_plural = _("TestPreps")

    def __str__(self):
        return f"{self.title}"


class TestPrepItem(PolymorphicModel, BaseModel):
    testprep = models.ForeignKey(
        TestPrep, on_delete=models.CASCADE, related_name="items"
    )
    time = models.DurationField(default=0)


class Section(TestPrepItem):
    title = models.CharField(_("title"), max_length=255)

    def get_parts(self):
        return self.parts.filter(status=True)

    def get_order(self):
        return self._order + 1

    def get_total_questions(self):
        return self.get_parts().aggregate(Sum("max_questions"))["max_questions__sum"]

    class Meta:
        verbose_name = _("Section")
        verbose_name_plural = _("Sections")
        order_with_respect_to = "testprep"

    def __str__(self):
        return f"{self.title}"


class Breake(TestPrepItem):
    class Meta:
        verbose_name = _("Breake")
        verbose_name_plural = _("Breakes")

    def __str__(self):
        return f"Breake for {self.testprep.title}"


class Part(BaseModel):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="parts")

    # subject = models.ForeignKey(
    #     "courses.Subject", on_delete=models.CASCADE, blank=True, null=True
    # )
    status = models.BooleanField(default=True)

    quizzes = models.ManyToManyField(Quiz, blank=True)
    questions = models.ManyToManyField(Question, blank=True)

    max_questions = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Max Questions"),
        help_text=_("Number of questions to be answered on each attempt."),
    )

    def get_part_results_by_user(self):
        return self.part_results.filter()

    def get_random_questions(self):
        quiz_ids = self.quizzes.filter().values_list("pk", flat=True)
        questions = Question.objects.filter(quiz__in=list(quiz_ids)).values_list(
            "pk", flat=True
        )

        items = list(questions)
        limit = min(self.max_questions, questions.count())

        if limit == 0:
            return Question.objects.none()

        random_items = random.sample(items, limit)
        random_objects = Question.objects.filter(pk__in=random_items).order_by("?")

        return random_objects

    def get_order(self):
        return self._order + 1

    def __str__(self):
        return f"Part {self._order + 1}"

    class Meta:
        verbose_name = _("Part")
        verbose_name_plural = _("Parts")
        order_with_respect_to = "section"


class TestprepResult(BaseModel):
    testprep = models.ForeignKey(
        TestPrep, on_delete=models.CASCADE, related_name="testprep_results"
    )
    total_score = models.PositiveIntegerField(default=0)
    results = models.JSONField(blank=True, null=True)
    STATUS = (
        ("initialized", "Initialized"),
        ("in-progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )
    status = models.CharField(max_length=14, choices=STATUS, default=STATUS[0][0])

    def get_parts(self):
        return self.testprep.parts.filter().all()

    def get_total_score_part(self):
        return self.get_parts().aggregate(Count("questions"))["questions__count"]

    def get_total_score_part_result(self):
        return (
            self.testprep_results.filter()
            .all()
            .aggregate(total_score=Sum("total_score"))["total_score"]
            or 0
        )

    def get_testprep_results_by_user(self):
        return self.testprep_results.filter().all()

    def get_part_results(self):
        return self.part_results.filter().all()

    def __str__(self):
        return f"#{self.pk}"

    class Meta:
        verbose_name = _("Testprep Result")
        verbose_name_plural = _("Testprep Results")


class TestprepItemResult(PolymorphicModel, BaseModel):
    testprep_item = models.ForeignKey(
        TestPrepItem,
        on_delete=models.CASCADE,
        related_name="%(class)s_testprep_item",
    )
    testprep_result = models.ForeignKey(
        TestprepResult,
        on_delete=models.CASCADE,
        related_name="%(class)s_testprep_result",
    )

    total_score = models.PositiveIntegerField(default=0)
    results = models.JSONField(blank=True, null=True)
    STATUS = (
        ("in-process", "In Process"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )
    status = models.CharField(max_length=14, choices=STATUS, default=STATUS[0][0])
    completed_at = models.DateTimeField(null=True, blank=True)


class BreakeResult(TestprepItemResult):
    pass


class SectionResult(TestprepItemResult):
    pass


class PartResult(BaseModel):
    section_result = models.ForeignKey(
        SectionResult,
        on_delete=models.CASCADE,
        related_name="testprepresult_partresults",
    )
    part = models.ForeignKey(
        Part, on_delete=models.CASCADE, related_name="part_partresults"
    )
    content = models.JSONField(null=True, blank=True)

    STATUS = (
        ("pending", "Pending"),
        ("scored", "Scored"),
        ("released", "Released"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    )
    status = models.CharField(max_length=14, choices=STATUS, default=STATUS[0][0])
    question_random_list = models.JSONField(null=True, blank=True)
    user_answers = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = _("Part Result")
        verbose_name_plural = _("Part Results")


class Bookmark(BaseModel):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="bookmark_questions"
    )
    part = models.ForeignKey(
        Part, on_delete=models.CASCADE, related_name="bookmark_parts"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bookmark_users"
    )
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
