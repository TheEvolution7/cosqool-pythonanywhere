from .serializers import *
from core.api.views import *

class ReportErrorViewSet(CoreViewSet):  
    queryset = ReportError.objects.all()  
    serializer_class = ReportErrorSerializer
    
class AdminReportErrorViewSet(AdminCoreViewSet, ReportErrorViewSet):  
    pass


    
class DashboardReportErrorViewSet(DashboardCoreViewSet, ReportErrorViewSet):
    pass