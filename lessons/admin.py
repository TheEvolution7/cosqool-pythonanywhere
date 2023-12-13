from django.contrib import admin
from .models import *
from core.admin import *
from django.utils.translation import gettext_lazy as _
from .forms import *


class LessonInline(nested_admin.NestedTabularInline):
    model = Lesson
    extra = 0


# class PracticeInline(nested_admin.NestedTabularInline):
#     model = Practice
#     extra = 0

# class PracticeQuestionInline(nested_admin.NestedTabularInline):
#     model = PracticeQuestion
#     extra = 0
#     form = PracticeQuestionAdminForm


class LessonItemInline(
    nested_admin.NestedStackedPolymorphicInline, admin.StackedInline
):
    model = LessonItem

    class LearnInline(
        nested_admin.NestedStackedPolymorphicInline.Child, admin.StackedInline
    ):
        model = Learn
        extra = 0
        # fields = (("title", "media", "status"),)
        show_change_link = True

    # class PracticeInline(
    #     nested_admin.NestedStackedPolymorphicInline.Child, TranslatableStackedInline
    # ):
    #     model = Practice
    #     extra = 0
    #     fields = (
    #         (
    #             "title",
    #             "score",
    #         ),
    #     )

    child_inlines = (
        LearnInline,
        # PracticeInline,
    )


class TranscriptAdminInline(
    nested_admin.NestedStackedInline, TranslatableStackedInline
):
    model = Transcript
    extra = 0
    # fields = (
    #     "title",
    #     "slug",
    #     "time",
    # )


class LearnItemInline(nested_admin.NestedStackedPolymorphicInline, admin.StackedInline):
    model = LearnItem

    class VideoInline(
        nested_admin.NestedStackedPolymorphicInline.Child, admin.StackedInline
    ):
        model = Video

    class TestInline(
        nested_admin.NestedStackedPolymorphicInline.Child, admin.StackedInline
    ):
        model = Test

    child_inlines = (
        VideoInline,
        TestInline,
    )


@admin.register(Learn)
class LearnAdmin(nested_admin.NestedPolymorphicModelAdmin, BaseCoreAdmin):
    inlines = (LearnItemInline,)

    list_display = (
        "__str__",
        "url",
        "score",
        "items",
    )

    @admin.display(description="Count Items")
    def items(self, obj):
        return f"{obj.items.count()}"
    
@admin.register(Lesson)
class LessonAdmin(nested_admin.NestedPolymorphicModelAdmin, BaseCoreAdmin):
    inlines = (LessonItemInline,)
    list_filter = ("section",)
    list_display = (
        "__str__",
        "section",
        "items",
        "created_by",
        "created_at",
    )

    @admin.display(description="Count Items")
    def items(self, obj):
        return f"{obj.items.count()}"
    
    search_fields = (
        "pk",
        "title",
    )
    # form = LessonAdminForm


# @admin.register(Practice)
# class PracticeAdmin(CoreAdmin):
#     inlines = (PracticeQuestionInline,)
#     list_filter = CoreAdmin.list_filter + ("lesson",)
#     form = PracticeAdminForm


@admin.register(Video)
class VideoAdmin(BaseCoreAdmin):
    list_filter = ("learn", "learn__lesson", )
    list_display = (
        "__str__",
        "learn", 
        "url",
    )
    search_fields = (
        "pk",
        # "title",
    )


@admin.register(Test)
class TestAdmin(BaseCoreAdmin):
    list_display = (
        "__str__",
        "learn", 
        "quiz",
    )
