from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User

def admin_log_context(request):
    user = request.user
    if user.is_authenticated and user.is_staff:
        admin_log = LogEntry.objects.filter(user_id=user.id).select_related('content_type', 'user')
        return {'admin_log': admin_log}
    return {'admin_log': None}
