from .base import *

from events.models import *
from django.core import serializers


class ScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/dashboards/schedule.html'

    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)
        calendar = Calendar.objects.filter().first()
        events = calendar.event_set.filter().all()
        calendar.events = serializers.serialize('json', events)

        get_context_data.update({'calendar': calendar})
        return get_context_data
