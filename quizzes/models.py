from django.utils.translation import gettext_lazy as _
from core.models import *
from ckeditor_uploader.fields import RichTextUploadingField
from model_utils.managers import InheritanceManager
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from django.core.validators import (
    MaxValueValidator,
)
from accounts.models import Teacher


class Quiz(models.Model):
    title = models.CharField(_("title"), max_length=255)

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        help_text=_("a description of the quiz"),
    )

    url = models.SlugField(
        max_length=60,
        blank=True,
        help_text=_("a user friendly url"),
        verbose_name=_("user friendly url"),
    )

    random_order = models.BooleanField(
        blank=False,
        default=False,
        verbose_name=_("Random Order"),
        help_text=_(
            "Display the questions in " "a random order or as they " "are set?"
        ),
    )

    max_questions = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Max Questions"),
        help_text=_("Number of questions to be answered on each attempt."),
    )

    answers_at_end = models.BooleanField(
        blank=False,
        default=False,
        help_text=_(
            "Correct answer is NOT shown after question."
            " Answers displayed at the end."
        ),
        verbose_name=_("Answers at end"),
    )

    exam_paper = models.BooleanField(
        blank=False,
        default=False,
        help_text=_(
            "If yes, the result of each"
            " attempt by a user will be"
            " stored. Necessary for marking."
        ),
        verbose_name=_("Exam Paper"),
    )

    single_attempt = models.BooleanField(
        blank=False,
        default=False,
        help_text=_(
            "If yes, only one attempt by"
            " a user will be permitted."
            " Non users cannot sit this exam."
        ),
        verbose_name=_("Single Attempt"),
    )

    pass_mark = models.SmallIntegerField(
        blank=True,
        default=0,
        verbose_name=_("Pass Mark"),
        help_text=_("Percentage required to pass exam."),
        validators=[MaxValueValidator(100)],
    )

    success_text = models.TextField(
        blank=True,
        help_text=_("Displayed if user passes."),
        verbose_name=_("Success Text"),
    )

    fail_text = models.TextField(
        verbose_name=_("Fail Text"), blank=True, help_text=_("Displayed if user fails.")
    )

    draft = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_("Draft"),
        help_text=_(
            "If yes, the quiz is not displayed"
            " in the quiz list and can only be"
            " taken by users who can edit"
            " quizzes."
        ),
    )

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_by = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, default=1, related_name="quizz_created_by"
    )
    updated_by = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, default=1, related_name="quizz_updated_by"
    )

    def get_questions(self):
        return self.questions.filter()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Quizz")
        verbose_name_plural = _("Quizzes")


class Question(models.Model):
    score = models.IntegerField(default=1)

    quiz = models.ForeignKey(
        Quiz, on_delete=models.DO_NOTHING, related_name="questions"
    )

    TYPES = [
        (
            _("Multiple Choice Questions"),
            (
                ("single_select", _("Single Select")),
                ("multi_select", _("Multi-Select")),
                ("dropdown", _("Dropdown Menu")),
                ("star_rating", _("Star Rating")),
                ("text_slider", _("Text Slider")),
                ("numeric_slider", _("Numeric Slider")),
                ("thumbs_up_down", _("Thumbs Up/Down")),
                ("matrix_table", _("Matrix Table")),
                ("rank_order", _("Rank Order")),
                ("image_based", _("Image/Picture Based")),
            ),
        ),
        ("TF", _("True/False")),
        ("SHORT", _("Short Answer")),
        ("ESSAY", _("Essay")),
    ]

    type = models.CharField(max_length=14, choices=TYPES, default=TYPES[0][0])

    content = RichTextUploadingField(_("content"), null=True, blank=True)

    figure = models.ImageField(
        upload_to="uploads/%Y/%m/%d", blank=True, null=True, verbose_name=_("Figure")
    )

    explanation = RichTextUploadingField(
        blank=True,
        help_text=_(
            "Explanation to be shown " "after the question has " "been answered."
        ),
        verbose_name=_("Explanation"),
    )

    objects = InheritanceManager()

    def answers(self):
        return self.answer_set.filter().all()

    def __str__(self):
        return f"{mark_safe(self.content)}"

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.DO_NOTHING, related_name="answers"
    )
    content = RichTextUploadingField(_("content"), null=True, blank=True)
    correct = models.BooleanField(_("correct"), default=False)

    image = models.ImageField(
        upload_to="uploads/%Y/%m/%d", blank=True, null=True, verbose_name=_("Image")
    )

    def __str__(self):
        return f"{mark_safe(self.content)}"
