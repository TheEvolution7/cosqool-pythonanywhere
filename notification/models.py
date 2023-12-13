from core.models import *
from accounts.models import *
from django.utils.translation import gettext_lazy as _

class Type(TranslatableModel, BaseModel):
    translations = translations()
    def get_notifications(self):
        return self.notifications.filter(status=True).all()
    class Meta:
        verbose_name = _("Type")
        verbose_name_plural = _("Types")
    
class Notification(TranslatableModel, BaseModel):
    translations = translations()
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="notifications")
    student = models.ManyToManyField("accounts.Student", through='NotificationStudent')
    
    class Meta:
        ordering = ["-id"]
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        
class NotificationStudent(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="notification_student_notifications")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="notification_student_students")
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
class NotificationTeacher(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="notification_teacher_notifications")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="notification_teacher_notifications")
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)