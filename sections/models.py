from django.db import models
from parler.models import TranslatableModel
from django.utils.translation import gettext_lazy as _
from core.models import *
from courses.models import Course
from accounts.models import Teacher
from polymorphic.managers import PolymorphicManager, PolymorphicQuerySet
from polymorphic.models import PolymorphicModel


class CustomManager(PolymorphicManager, TranslatableManager):
    def manager_only_method(self):
        return


class CustomQuerySet(PolymorphicQuerySet, TranslatableQuerySet):
    def manager_and_queryset_method(self):
        return


class Section(models.Model):
    title = models.CharField(_("title"), max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=1, related_name="section_created_by")
    updated_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=1, related_name="section_updated_by")

    class Meta:
        verbose_name = _("Section")
        verbose_name_plural = _("Sections")

    def items(self):
        return self.section_items.filter().all()

    def count_lesson(self):
        return self.items

    def __str__(self):
        return f"{self.title}"


from django.db.models import Sum


class SectionItem(PolymorphicModel):
    title=models.CharField(_('title'), max_length=255)
    objects = CustomManager.from_queryset(CustomQuerySet)()
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="section_items"
    )

    def get_lessons(self):
        return self.lessons.filter().all()

    def get_total_score_lesson(self):
        return (
            self.get_lessons().aggregate(total_score=Sum("learn__score"))["total_score"]
            or 0
        )

    def get_total_score_lesson_by_user(self):
        list = self.lessons.select_related("lesson")
        total = 0
        for item in list:
            total += item.get_learnscore_by_user()
        return total

    def get_total_score_quiz(self):
        return (
            self.get_questions().aggregate(total_score=Sum("score"))["total_score"] or 0
        )

    class Meta:
        verbose_name = _("Section Item")
        verbose_name_plural = _("Section Items")

    def __str__(self):
        return f"{self.title}"
