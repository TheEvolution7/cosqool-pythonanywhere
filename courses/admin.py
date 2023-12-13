from django.contrib import admin
from .models import *
from core.admin import *
from django.utils.translation import gettext_lazy as _
from sections.models import *
from lessons.models import *

# from quizzes.models import *
from lessons.admin import *
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicParentModelAdmin,
    PolymorphicInlineSupportMixin,
)


class SectionItemAdminInline(
    nested_admin.NestedStackedPolymorphicInline, TranslatableStackedInline
):
    model = SectionItem

    class LessonInline(
        nested_admin.NestedStackedPolymorphicInline.Child, TranslatableStackedInline
    ):
        model = Lesson
        fields = (
            (
                "title",
                "status",
            ),
        )
        # inlines = (LessonItemInline, )

    # class QuizInline(nested_admin.NestedStackedPolymorphicInline.Child, TranslatableStackedInline):
    #     model = Quiz
    #     fields = (('title', 'status', ), )

    child_inlines = (
        LessonInline,
        # QuizInline
    )


class SectionInline(
    nested_admin.NestedStackedInline,
    admin.StackedInline,
    PolymorphicInlineSupportMixin,
):
    model = Section
    # inlines = (SectionItemAdminInline, )
    fields = (
        (
            "title",
            # "status",
        ),
    )
    extra = 0


from django.forms import ModelChoiceField


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.pk


# class CourseForm(CoreBaseForm):
#     teacher_choices = [
#         (teacher.pk, teacher.get_full_name) for teacher in Teacher.objects.all()
#     ]
#     teacher = forms.ChoiceField(choices=teacher_choices)


from .resources import *


@admin.register(Course)
class CourseAdmin(CoreAdmin, nested_admin.NestedPolymorphicModelAdmin):
    inlines = (SectionInline, )
    resource_classes = [CourseResource]


@admin.register(Category)
class CategoryAdmin(CoreCategoryAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(CoreAdmin):
    pass


@admin.register(Grade)
class GradeAdmin(CoreAdmin):
    pass


