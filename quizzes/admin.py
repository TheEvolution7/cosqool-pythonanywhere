from django.contrib import admin
from .models import *
from core.admin import *
from django.utils.translation import gettext_lazy as _


@admin.register(Quiz)
class QuizAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    list_display = ('__str__', 'total_questions', 'created_by', 'created_at', )
    search_fields = ('pk', 'title', )
    
    @admin.display(description="Total Questions")
    def total_questions(self, obj):
        return f"{obj.question_set.count()}"
    
class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    inlines = (AnswerInline, )

    list_display = ('__str__', 'type', 'score', 'answer_tag', 'action_tag', )
    list_filter = ('quiz', 'type', )
    search_fields = ('pk', 'content', )
    
    @admin.display(description='answers')
    def answer_tag(self, obj):
        return obj.answer_set.count()
    
    @admin.display(description='actions')
    def action_tag(self, obj):
        return action_tag(self, obj)


@admin.register(Answer)
class AnswerAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    list_display = ('__str__', 'question_tag', 'correct', 'action_tag', )
    list_filter = ('question', )
    search_fields = ('pk', 'content', )
    
    @admin.display(description='question')
    def question_tag(self, obj):
        return obj.question
    
    @admin.display(description='actions')
    def action_tag(self, obj):
        return action_tag(self, obj)
