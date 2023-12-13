from .models import *
from core.admin import *
from django.utils.translation import gettext_lazy as _

# class AnswerInline(nested_admin.NestedTabularInline, TranslatableTabularInline):
#     model = Answer
#     extra = 0
#     fields = ('content', 'correct', 'status', )


# class QuestionInline(nested_admin.NestedTabularInline, TranslatableTabularInline):
#     model = Question
#     extra = 0
#     fields = ('content', 'status', 'position', )
#     # inlines = (AnswerInline, )


class PartInline(nested_admin.NestedTabularInline):
    model = Part
    extra = 0
    # inlines = (QuestionInline, )
    fields = ('subject', 'time', 'status', )
    show_change_link = True


@admin.register(TestPrep)
class TestPrepAdmin(CoreAdmin):
    inlines = (PartInline, )

# class PartQuestionInline(nested_admin.NestedTabularInline):
#     model = PartQuestion
#     extra = 0
        
@admin.register(Part)
class PartAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin,):
    # inlines = (PartQuestionInline, )
    list_display = ['str_tag', 'testprep', 'subject', 'status', 'action_tag']
    list_filter = ('subject', 'testprep', 'status', )
    search_fields = ('id', 'part__title', )

# @admin.register(Question)
# class QuestionAdmin(CoreAdmin):
#     inlines = (AnswerInline, )
#     list_display = ['str_tag', 'part',
#                     'status_tag', 'action_tag']
#     list_filter = ('part', 'part__testprep')
#     base_fieldsets = ((None, {
#         'fields': ('content', )
#     }),)

#     def get_prepopulated_fields(self, request, obj=None):
#         return {}

class PartResultInline(nested_admin.NestedTabularInline):
    model = PartResult
    extra = 0
    # inlines = (QuestionInline, )
    fields = ('part', 'total_score', 'status', 'created_at', )
    readonly_fields = ('part', 'total_score', 'status', 'created_at', )
    can_delete = False
    max_num = 0
    show_change_link = True
    
@admin.register(TestprepResult)
class TestprepResultAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    list_display = ['str_tag', 'testprep',
                    'student_tag', 'status_tag', 'total_score', 'created_at', 'action_tag']
    
    @admin.display(description='status')
    def status_tag(self, obj):
        return status_tag(self, obj)
    
    @admin.display(description='student')
    def student_tag(self, obj):
        return mark_safe(render_to_string('admin/tags/student_tag.html', {'obj': obj.user.student}))
    
    base_fieldsets = ((None, {
        'fields': ('total_score', )
    }),)
    
    inlines = (PartResultInline, )

@admin.register(PartResult)
class PartResultAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    list_display = ['str_tag', 'testprep_result', 'part', 'status_tag', 'total_score', 'created_at', 'action_tag']
    
    @admin.display(description='status')
    def status_tag(self, obj):
        return status_tag(self, obj)
    
    list_filter = ('testprep_result', 'part', )
    search_fields = ('pk', 'testprep__translations__title',
                     'part__translations__title', )
    date_hierarchy = ('created_at')
    base_fieldsets = ((None, {
        'fields': ('total_score', )
    }),)

    def get_prepopulated_fields(self, request, obj=None):
        return {}

@admin.register(Bookmark)
class BookmarkAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    list_display = ['str_tag', 'action_tag']
    base_fieldsets = ((None, {
        'fields': ('question', )
    }),)
    
# @admin.register(Answer)
# class AnswerAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
#     list_display = ['str_tag', 'action_tag']
