from rest_framework import viewsets, renderers, response, filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class CoreViewSet(viewsets.ModelViewSet): 
    ordering_fields = '__all__'
    search_fields = ['id']
    filterset_fields = ['id']
    
    
    
class AdminCoreViewSet(CoreViewSet):  
    pass
    
class DashboardCoreViewSet(CoreViewSet):  
    pass

class InstructorViewSet(CoreViewSet):  
    pass
    
    