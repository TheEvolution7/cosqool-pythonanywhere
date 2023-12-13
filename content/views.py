from django.views import generic
from .models import *

class PlaylistListView(generic.ListView):
    model = Playlist
    
class PlaylistDetailView(generic.DetailView):
    model = Playlist
    
class PlaylistUpdateView(generic.UpdateView):
    model = Playlist
    
class PlaylistCreateView(generic.CreateView):
    model = Playlist
    
class PlaylistDeleteView(generic.DeleteView):
    model = Playlist

    
from django.http import Http404
from rest_framework import permissions

from rest_framework.views import APIView
from content.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import renderers

class PlaylistList(APIView):
    renderer_classes = [renderers.JSONRenderer]
    def get(self, request, format=None):
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True,)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import permissions

class PlaylistDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        try:
            return Playlist.objects.get(pk=pk)
        except Playlist.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PlaylistSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PlaylistSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import renderers

from rest_framework import permissions

class PlaylistViewSet(viewsets.ModelViewSet):    
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs
    


from .serializers import PlaylistItemSerializer, PlaylistItem
from core.api.views import *

class PlaylistItemViewSet(CoreViewSet):  
    queryset = PlaylistItem.objects.all()  
    serializer_class = PlaylistItemSerializer
    filterset_fields = CoreViewSet.filterset_fields + ['playlist']
    
class AdminPlaylistItemViewSet(AdminCoreViewSet, PlaylistItemViewSet): 
    def list(self, request, format=None):
        
        if request.accepted_renderer.format == 'html':
            data = {}
            return Response(data, template_name='./playlist_file_list.html')

        return super().list(request, format)
    
