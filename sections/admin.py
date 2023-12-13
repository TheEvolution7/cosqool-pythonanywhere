from django.contrib import admin
from .models import *
import nested_admin
from core.admin import *
from lessons.models import *
from lessons.models import *

# from quizzes.models import *
from lessons.admin import *

from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionModelAdmin
from .resources import *


class SectionItemAdminInline(
    nested_admin.NestedStackedPolymorphicInline, admin.StackedInline
):
    model = SectionItem

    class LessonInline(
        nested_admin.NestedStackedPolymorphicInline.Child, admin.StackedInline
    ):
        model = Lesson
        # fields = (
        #     (
        #         "title",
        #         "status",
        #     ),
        # )
        inlines = (LessonItemInline,)

    # class QuizInline(
    #     nested_admin.NestedStackedPolymorphicInline.Child, admin.StackedInline
    # ):
    #     model = Quiz
    #     fields = (
    #         (
    #             "title",
    #             "status",
    #         ),
    #     )

    child_inlines = (LessonInline,)


# class SectionAdminForm(CoreBaseForm):
#     class Meta:
#         model = Section
#         fields = "__all__"
#         widgets = {
#             "course": forms.Select(attrs={"data-control": "select2"}),
#         }


# @admin.register(SectionItem)
# class SectionItemAdmin(BaseCoreAdmin, nested_admin.NestedPolymorphicModelAdmin):
#     resource_classes = [SectionItemResource]
#     inlines = (LessonInline, )


@admin.register(Section)
class SectionAdmin(BaseCoreAdmin, nested_admin.NestedPolymorphicModelAdmin):
    inlines = (SectionItemAdminInline,)

    list_display = (
        "__str__",
        "course",
        "items",
        "created_by",
        "created_at",
    )

    @admin.display(description="Count Items")
    def items(self, obj):
        return f"{obj.section_items.count()}"
