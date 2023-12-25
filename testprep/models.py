from ckeditor import fields
from core.fields import Select2Field
from accounts.models import *
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import *
from courses.models import Course

from django.db.models import Sum, Count
from django.utils.html import strip_tags
from django.utils.text import Truncator

class TestPrep(TranslatableModel, BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    translations = translations()
    course = models.ForeignKey(
        Course, models.DO_NOTHING, null=True, blank=True, related_name='testprep')

    class Meta:
        verbose_name = _("Test Prep")
        verbose_name_plural = _("Test Preps")

    def get_parts(self):
        return self.parts.filter(status=True).all()

    def get_total_questions(self):
        return self.get_parts().aggregate(Count('questions'))['questions__count']

    def get_total_duration_parts(self):
        return self.get_parts().aggregate(total_duration_part=Sum("time"))['total_duration_part']

    def get_total_score_part(self):
        return self.get_parts().aggregate(Count('questions'))['questions__count']

    def get_total_score_part_result(self):
        return self.testprep_results.filter().aggregate(total_score=Sum("score"))['total_score'] or 0

    def get_testprep_results_by_user(self):
        return self.testprep_results.filter().all()

    class Meta:
        verbose_name = _("TestPrep")
        verbose_name_plural = _("TestPreps")

class Part(TranslatableModel, BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    translations = translations()
    testprep = models.ForeignKey(
        TestPrep, on_delete=models.CASCADE, related_name="parts")
    time = models.DurationField(
        help_text="Duration of the quiz in seconds", default="1")

    subject = models.ForeignKey("courses.Subject", on_delete=models.CASCADE)

    def get_part_results_by_user(self):
        return self.part_results.filter().all()

    def get_questions(self):
        return self.questions.filter(status=True).all()

    def get_order(self):
        return self._order + 1
    class Meta:
        verbose_name = _("Part")
        verbose_name_plural = _("Parts")
        order_with_respect_to = "testprep"


class Question(TranslatableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    translations = TranslatedFields(
        content=RichTextUploadingField(
            _('content'), null=True, blank=True),
    )

    part = models.ForeignKey(
        Part, on_delete=models.CASCADE, related_name="questions")
    position = models.IntegerField(_('Position'), null=True, default=0)
    status = models.BooleanField(default=True)
    score = models.PositiveIntegerField(default=1)

    TYPES = [
        (
            _("Multiple Choice Questions"),
            (
                ('single_select', _('Single Select')),
                ('multi_select', _('Multi-Select')),
                ('dropdown', _('Dropdown Menu')),
                ('star_rating', _('Star Rating')),
                ('text_slider', _('Text Slider')),
                ('numeric_slider', _('Numeric Slider')),
                ('thumbs_up_down', _('Thumbs Up/Down')),
                ('matrix_table', _('Matrix Table')),
                ('rank_order', _('Rank Order')),
                ('image_based', _('Image/Picture Based')),
            ),
        ),
        ('TF', _('True/False')),
        ('SHORT', _('Short Answer')),
        ('ESSAY', _('Essay')),
    ]

    # test  = Select2Field(max_length=14, choices=TYPES, default=TYPES[0][0])
    type = models.CharField(max_length=14, choices=TYPES, default=TYPES[0][0])

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def get_answers(self):
        return self.answers.filter(status=True).all()

    def get_order(self):
        return self._order + 1
    def __str__(self):
        content = self.content
        content = Truncator(self.content)
        content = strip_tags(content)
        return f"{content}"

    class Meta:
        order_with_respect_to = "part"
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")


class Answer(TranslatableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    translations = TranslatedFields(
        content=fields.RichTextField(
            _('content'), null=True, blank=True, config_name="ckeditor"),
    )
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers")
    position = models.IntegerField(_('Position'), null=True, default=0)
    status = models.BooleanField(default=True)

    def get_result_by_user(self):
        return self

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        order_with_respect_to = "question"

    # def __str__(self):
    #     return f"{strip_tags(self.content)}"

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")


class TestprepResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    testprep = models.ForeignKey(
        TestPrep, on_delete=models.CASCADE, related_name="testprep_results")
    total_score = models.PositiveIntegerField(default=0)

    STATUS = (
        ('pending', _('Pending')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
    )
    status = models.CharField(
        max_length=11, choices=STATUS, default=STATUS[0][0])

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    def get_parts(self):
        return self.testprep.parts.filter().all()

    def get_total_score_part(self):
        return self.get_parts().aggregate(Count('questions'))['questions__count']

    def get_total_score_part_result(self):
        return self.testprep_results.filter().all().aggregate(total_score=Sum("total_score"))['total_score'] or 0

    def get_testprep_results_by_user(self):
        return self.testprep_results.filter().all()

    def get_part_results(self):
        return self.part_results.filter().all()
    def __str__(self):
        return f"#{self.pk}"

    class Meta:
        verbose_name = _("Testprep Result")
        verbose_name_plural = _("Testprep Results")


class PartResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    testprep_result = models.ForeignKey(
        TestprepResult, on_delete=models.CASCADE, related_name="part_results")
    part = models.ForeignKey(
        Part, on_delete=models.CASCADE, related_name="part_part_results")
    content = models.JSONField(null=True, blank=True)

    total_score = models.PositiveIntegerField(default=0)

    STATUS = (
        ('pending', _('Pending')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
    )
    status = models.CharField(
        max_length=11, choices=STATUS, default=STATUS[0][0])

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)



    class Meta:
        verbose_name = _("Part Result")
        verbose_name_plural = _("Part Results")

    def __str__(self):
        return f"#{self.pk}"

class Bookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="testprep_bookmark_questions")
    part = models.ForeignKey(
        Part, on_delete=models.CASCADE, related_name="testprep_bookmark_parts")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="testprep_bookmark_users")
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
