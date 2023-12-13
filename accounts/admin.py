from django.contrib.auth.models import Group as BaseGroup
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import *
from core.admin import *
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse
from django.template.loader import render_to_string


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        "str_tag",
        "name_tag",
        "email",
        "is_staff_tag",
        "last_login",
        "action_tag",
    )

    @admin.display(description="Staff status")
    def is_staff_tag(self, obj):
        if obj.is_staff:
            return mark_safe(
                '<div class="rounded-circle bg-success w-15px h-15px"></div>'
            )
        return mark_safe('<div class="rounded-circle bg-danger w-15px h-15px"></div>')

    @admin.display(description="name")
    def name_tag(self, obj):
        return obj.get_full_name()

    @admin.display(description="username")
    def str_tag(self, obj):
        return mark_safe(
            render_to_string("admin/tags/user_str_tag.html", {"obj": obj, "self": self})
        )

    @admin.display(description="actions")
    def action_tag(self, obj):
        return action_tag(self, obj)


@admin.register(Student)
class StudentAdmin(BaseCoreAdmin):
    list_filter = ("gender",)
    search_fields = [
        "id",
        "phone_number",
    ]
    list_display = (
        "str_tag",
        "user",
        "phone_number",
        "created_at",
        "updated_at",
        "action_tag",
    )

    @admin.display(description="Student")
    def str_tag(self, obj):
        return mark_safe(
            render_to_string("admin/tags/student_str_tag.html", {"obj": obj})
        )

    base_fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "gender",
                    "phone_number",
                    "language",
                )
            },
        ),
        (
            _("Avatar"),
            {
                "fields": ("avatar",),
            },
        ),
        (
            _("User"),
            {
                "fields": ("user",),
            },
        ),
    )

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path(
                "<path:object_id>/view/",
                self.admin_site.admin_view(self.view, cacheable=True),
                name="users_user_view",
            )
        ]

        return my_urls + urls

    def view(self, request, object_id):
        context = dict(
            self.admin_site.each_context(request),
        )
        context.update({"object": Student.objects.filter(pk=object_id).first()})
        return TemplateResponse(request, "admin/users/view.html", context)

    @admin.display(description="actions")
    def action_tag(self, obj):
        return action_tag(self, obj)


@admin.register(Teacher)
class TeacherAdmin(BaseCoreAdmin):
    list_filter = ("gender",)
    search_fields = [
        "id",
        "phone_number",
    ]
    list_display = (
        "str_tag",
        "user",
        "phone_number",
        "created_at",
        "updated_at",
        "action_tag",
    )

    @admin.display(description="Student")
    def str_tag(self, obj):
        return mark_safe(
            render_to_string("admin/tags/student_str_tag.html", {"obj": obj})
        )

    base_fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "gender",
                    "phone_number",
                    "language",
                )
            },
        ),
        (
            _("Avatar"),
            {
                "fields": ("avatar",),
            },
        ),
        (
            _("User"),
            {
                "fields": ("user",),
            },
        ),
    )


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_filter = ("gender",)
    search_fields = [
        "id",
        "phone_number",
    ]
    list_display = (
        "__str__",
        "action_tag",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "gender",
                    "phone_number",
                    "language",
                    "headline",
                    "biography",
                    "website",
                    ("facebook_url", "twitter_url"),
                    ("linkedin_url", "youtube_url"),
                )
            },
        ),
        (_("Avatar"), {"fields": ("avatar",), "classes": ("show",)}),
        (_("User"), {"fields": ("user",), "classes": ("show",)}),
    )

    @admin.display(description="actions")
    def action_tag(self, obj):
        return action_tag(self, obj)


admin.site.unregister(BaseGroup)


@admin.register(Group)
class GroupAdmin(GroupAdmin):
    list_display = (
        "__str__",
        "permission_tag",
        "user_tag",
        "action_tag",
    )

    @admin.display(description="actions")
    def action_tag(self, obj):
        return action_tag(self, obj)

    @admin.display(description="Permission Count")
    def permission_tag(self, obj):
        return obj.permissions.count()

    @admin.display(description="User Count")
    def user_tag(self, obj):
        return obj.user_set.count()


@admin.register(Avatar)
class AvatarAdmin(BaseCoreAdmin):
    list_display = (
        "image_tag",
        "action_tag",
    )

    @admin.display(description="")
    def image_tag(self, obj):
        return mark_safe(
            f'<div class="symbol symbol-50px"><span class="symbol-label" style="background-image:url({obj.image.url});"></span></div>'
        )


@admin.register(Enrollment)
class EnrollmentAdmin(BaseCoreAdmin):
    base_fieldsets = (
        (
            None,
            {
                "fields": (
                    "status",
                    "completed_at",
                    "drop_reason",
                )
            },
        ),
    )

    list_display = (
        "id",
        "status",
        "created_at",
        "action_tag",
    )
    search_fields = ("pk",)
