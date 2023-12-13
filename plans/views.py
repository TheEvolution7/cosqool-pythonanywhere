from django.shortcuts import render

from .serializers import PlanSerializer, Plan
from core.api.views import *

class PlanViewSet(CoreViewSet):  
    queryset = Plan.objects.all()  
    serializer_class = PlanSerializer
    
class AdminPlanViewSet(AdminCoreViewSet, PlanViewSet):  
    pass