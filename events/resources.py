from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import *

class EventResource(resources.ModelResource):
    
    calendar = fields.Field(
        column_name='calendar',
        attribute='calendar',
        widget=ForeignKeyWidget(Calendar, field='title'))
    
    class Meta:
        model = Event
        import_id_fields = ('id',)
        fields = ('id','calendar',)