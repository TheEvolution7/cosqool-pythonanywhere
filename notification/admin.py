from .models import *
from django.utils.translation import gettext_lazy as _

from core.admin import *

class NotificationStudentInline(nested_admin.NestedTabularInline):
    model = NotificationStudent
    extra = 0

@admin.register(Notification)
class NotificationAdmin(CoreAdmin):
    pass


    
@admin.register(NotificationStudent)
class NotificationStudentAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    list_display = ()
    list_filter = ()

@admin.register(NotificationTeacher)
class NotificationTeacherAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    list_display = ()
    list_filter = ()
    
@admin.register(Type)
class TypeAdmin(CoreAdmin):
    pass

    
