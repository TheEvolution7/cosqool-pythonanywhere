from .models import *
from core.resources import *

class CourseResource(BaseResource):
    subject = Field(attribute='title', column_name='subject__title')
    grade = Field(attribute='title', column_name='grade__title')
    teacher = Field(attribute='teacher__user__email', column_name='teacher__user__email')
    
    class Meta:
        model = Course
        
    
        
