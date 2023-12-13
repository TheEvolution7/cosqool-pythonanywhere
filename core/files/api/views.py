from ..serializers import FileSerializer, File
from core.api.views import *

class FileViewSet(CoreViewSet):  
    queryset = File.objects.all()  
    serializer_class = FileSerializer
    
class AdminFileViewSet(AdminCoreViewSet, FileViewSet):  
    pass