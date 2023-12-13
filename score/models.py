# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from core.models import *

# class Score(models.Model):
#     student = models.ForeignKey("accounts.Student", on_delete=models.DO_NOTHING)
#     score = models.IntegerField(default=0)
    
#     created_at = models.DateTimeField(_('created at'), auto_now_add=True)
#     updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
#     class Meta:
#         abstract = True
    
        
# class LearnScore(Score):
#     learn = models.ForeignKey("lessons.Learn", on_delete=models.DO_NOTHING)
    
#     class Meta:
#         verbose_name = _("Learn Score")
#         verbose_name_plural = _("Learn Scores")

# # class PracticeScore(Score):
# #     practice = models.ForeignKey("lessons.Practice", on_delete=models.DO_NOTHING)
    
# #     class Meta:
# #         verbose_name = _("Practice Score")
# #         verbose_name_plural = _("Practice Scores")

# class QuizScore(Score):
#     quiz = models.ForeignKey("quizzes.Quiz", on_delete=models.DO_NOTHING)
    
#     class Meta:
#         verbose_name = _("Quiz Score")
#         verbose_name_plural = _("Quiz Scores")

# class QuestionScore(Score):
#     question = models.ForeignKey("quizzes.Question", on_delete=models.DO_NOTHING)
#     answer = models.ForeignKey("quizzes.Answer", on_delete=models.DO_NOTHING, null=True, blank=True)
#     content = models.TextField(blank=True)
#     class Meta:
#         verbose_name = _("Question Score")
#         verbose_name_plural = _("Question Scores")