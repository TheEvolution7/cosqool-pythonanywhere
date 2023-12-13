from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
        
class EventObject(models.Model):
    content = models.JSONField(null=True, blank=True)
    CHOICES = (
        ('default', 'Default'),
        ('custom', 'Custom'),
    )
    
    type = models.CharField(max_length=10, choices=CHOICES, default=CHOICES[0])
    def __str__(self):
        return f"{self.pk}"
    
    class Meta:
        verbose_name = _("Event Object")
        verbose_name_plural = _("Event Objects")
        
class Calendar(models.Model):
    title = models.CharField(max_length=255)
    def default_calendar_settings():
        return {
            'initialView': 'dayGridMonth',
            'droppable': False,
            'dayMaxEvents': True,
            'editable': False,
            'navLinks': True,
            'selectMirror': False,
            'headerToolbar': {
                'left': 'prev,next today',
                'center': 'title',
                'right': 'dayGridMonth,dayGridDay,listYear'
            },
            'contentHeight': 'auto'
        }
    content = models.JSONField(null=True, blank=True, default=default_calendar_settings)
    
    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = _("Calendar")
        verbose_name_plural = _("Calendars")

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event_object = models.ForeignKey(EventObject, on_delete=models.CASCADE, null=True, blank=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, null=True, blank=True)
    
    content = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.pk}"
    
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")