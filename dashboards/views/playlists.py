from .base import *
from playlists.models import *
from playlists.views import *

class PlaylistUpdateDashboardForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('title', )
        
class PlaylistCreateDashboardForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('title', )
    
    
class DashboardPlaylistListView(DashboardView, PlaylistListView):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user).all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        playlists = self.get_queryset()
        
        playlist_update_forms = []
        for playlist in playlists:
            form = PlaylistUpdateDashboardForm(instance=playlist)
            playlist_update_forms.append(form)
        
        context.update({
            "playlist_update_dashboard_forms": playlist_update_forms
        })
        return context

class DashboardPlaylistDetailView(DashboardView, PlaylistDetailView):
    def get_context_data(self, **kwargs):
        qs = super().get_context_data(**kwargs)
        videos = self.get_object().get_videos().order_by("-pk")
        qs.update({'videos': videos})

        paginator = Paginator(videos, 1)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        qs.update({'page_obj': page_obj})

        return qs

class DashboardPlaylistUpdateView(SuccessMessageMixin, DashboardView, PlaylistUpdateView):
    success_message = "%(title)s was updated successfully"
    form_class = PlaylistUpdateDashboardForm
    
    def get_success_url(self):
        return reverse('dashboards:playlists:index')


class DashboardPlaylistDeleteView(SuccessMessageMixin, DashboardView, PlaylistDeleteView):
    success_message = "This was deleted successfully"

    def get_success_url(self):
        return reverse('dashboards:playlists:index')

from rest_framework.views import APIView
from content.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import renderers

class DashboardPlaylistCreateView(APIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    model = Playlist
     
    def get(self, request, format=None):
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        params = request.data
        user = self.request.user
        params.update({"user":user.pk})
        serializer = PlaylistSerializer(data=params)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlaylistCreateAPIView(generics.CreateAPIView):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    model = Playlist

    
     
    def post(self, request, format=None):
        params = request.data
        user = self.request.user
        params.update({"user":user.pk})
        serializer = PlaylistSerializer(data=params)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PlaylistUpdateAPIView(APIView):

    def put(self, request, pk, format=None):
        playlist_id = request.data.get('playlist')
        playlist = Playlist.objects.get(pk=playlist_id)
        data = {
            "user": request.user.pk,
            "title": playlist.title,
            "videos": playlist.videos.add(pk)
        }
        serializer = PlaylistSerializer(playlist, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

