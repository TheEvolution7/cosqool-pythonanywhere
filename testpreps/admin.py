from .models import (
    TestPrep,
    TestPrepItem,
    Section,
    Breake,
    Part,
    TestprepResult,
    SectionResult,
    PartResult,
    Bookmark,
    BreakeResult,
)
from core.admin import *
from django.utils.translation import gettext_lazy as _


class PartInline(nested_admin.NestedTabularInline):
    model = Part
    extra = 0
    show_change_link = True


class TestPrepItemInline(
    nested_admin.NestedStackedPolymorphicInline, admin.StackedInline
):
    model = TestPrepItem

    class SectionInline(
        nested_admin.NestedStackedPolymorphicInline.Child, admin.StackedInline
    ):
        model = Section

    class BreakeInline(
        nested_admin.NestedStackedPolymorphicInline.Child, admin.StackedInline
    ):
        model = Breake

    child_inlines = (
        SectionInline,
        BreakeInline,
    )


@admin.register(TestPrep)
class TestPrepAdmin(nested_admin.NestedPolymorphicModelAdmin, BaseCoreAdmin):
    inlines = (TestPrepItemInline,)
    list_display = ("__str__", "slug", "status", "created_by", "created_at", "items", )

    @admin.display()
    def items(self, obj):
        return obj.items.count()


@admin.register(Section)
class SectionAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    inlines = (PartInline,)

    list_display = ("__str__", "testprep", "status", "time", "created_by", "created_at", "parts", )

    @admin.display()
    def parts(self, obj):
        return obj.parts.count()

@admin.register(Breake)
class BreakeAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    list_display = ("__str__", "testprep", "status", "time" ,"created_by", "created_at", )


@admin.register(Part)
class PartAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    list_display = ("__str__", "section", "status", "created_by", "created_at", )


# class PartResultInline(nested_admin.NestedTabularInline):
#     model = PartResult
#     extra = 0
#     # inlines = (QuestionInline, )
#     fields = (
#         "part",
#         "total_score",
#         "status",
#         "created_at",
#     )
#     readonly_fields = (
#         "part",
#         "total_score",
#         "status",
#         "created_at",
#     )
#     can_delete = False
#     max_num = 0
#     show_change_link = True

from django_json_widget.widgets import JSONEditorWidget
from django.db import models

@admin.register(TestprepResult)
class TestprepResultAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    list_display = [
        "str_tag",
        "testprep",
        # "student_tag",
        "status_tag",
        "total_score",
        "created_at",
        "action_tag",
    ]

    @admin.display(description="status")
    def status_tag(self, obj):
        return status_tag(self, obj)

    # @admin.display(description="student")
    # def student_tag(self, obj):
    #     return mark_safe(
    #         render_to_string("admin/tags/student_tag.html", {"obj": obj.user.student})
    #     )

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }

    # inlines = (PartResultInline,)

@admin.register(SectionResult)
class SectionResultAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    pass

@admin.register(PartResult)
class PartResultAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    pass

@admin.register(BreakeResult)
class BreakeResultAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    pass

@admin.register(Bookmark)
class BookmarkAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    list_display = ["str_tag", "action_tag"]
    base_fieldsets = ((None, {"fields": ("question",)}),)
