from django import forms

from core.admin import CoreBaseForm, CoreForm
from .models import Lesson, Learn

class LessonAdminForm(CoreForm):
    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {
            "section": forms.Select(attrs={"data-control": "select2"}),
        }    
        
# class PracticeAdminForm(CoreBaseForm):
#     class Meta:
#         model = Practice
#         fields = '__all__'
#         widgets = {
#             "lesson": forms.Select(attrs={"data-control": "select2"}),
#         }  
        
# class PracticeQuestionAdminForm(forms.ModelForm):
#     class Meta:
#         model = PracticeQuestion
#         fields = '__all__'
#         widgets = {
#             "question": forms.Select(attrs={"data-control": "select2"}),
#         }    