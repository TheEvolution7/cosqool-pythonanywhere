from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import File
from .serializers import FileSerializer
class FileListView(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
class FileDetailView(APIView):
    pass
    