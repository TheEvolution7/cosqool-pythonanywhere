from django.db import models
from parler.models import TranslatableModel
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from core.models import *


class Category(MPTTModel, TranslatableModel, BaseModel):
    translations = translations()
    objects = objects = CategoryManager()
    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING,
                            null=True, blank=True, related_name='children')

    class MPTTMeta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Grade(TranslatableModel, BaseModel):
    translations = translations()

    category = TreeForeignKey(
        Category,
        on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = _("Grade")
        verbose_name_plural = _("Grades")


class Subject(TranslatableModel, BaseModel):
    translations = translations()

    grades = models.ManyToManyField(
        Grade)

    def courses(self):
        return self.course_set.filter().all()

    def grade(self):
        return self.grades.all()[0]

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

from accounts.models import Teacher
class Course(TranslatableModel, BaseModel):
    translations = translations()
    
    subject = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    grade = models.ForeignKey(
        Grade, on_delete=models.DO_NOTHING, null=True, blank=True)

    teacher = models.ForeignKey(
        Teacher, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def sections(self):
        return self.section_set.filter().all()
