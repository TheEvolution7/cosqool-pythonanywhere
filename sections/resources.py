from .models import *
from core.resources import *

class SectionResource(BaseResource):
    
    # course = Field(attribute='course__title', column_name='course__title')
    class Meta:
        model = Section
        
class SectionItemResource(BaseResource):
    
    # section = Field(attribute='section__title', column_name='section__title')
    class Meta:
        model = SectionItem