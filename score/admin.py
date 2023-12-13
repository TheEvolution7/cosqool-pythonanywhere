# from .models import *
# from core.admin import *
# from django.utils.translation import gettext_lazy as _

# class ScoreAdmin(BaseCoreAdmin):
#     base_fieldsets = ((None, {
#         'fields': ('score', )
#     }),)
    
#     list_display = ("id", "score", "created_at", "action_tag", )
#     search_fields = ("pk", "student", "score", )
    
# @admin.register(LearnScore)
# class LearnScoreAdmin(ScoreAdmin):
#     pass

# # @admin.register(PracticeScore)
# # class PracticeScoreAdmin(ScoreAdmin):
# #     pass

# # @admin.register(QuizScore)
# # class QuizScoreAdmin(ScoreAdmin):
# #     pass

# # @admin.register(QuestionScore)
# # class QuestionScoreAdmin(ScoreAdmin):
# #     base_fieldsets = ((None, {
# #         'fields': ("score", "answer", "content", )
# #     }),)