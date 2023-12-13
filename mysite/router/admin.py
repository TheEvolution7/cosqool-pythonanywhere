from rest_framework import routers

from core.files.api.views import AdminFileViewSet
from content.views import AdminPlaylistItemViewSet, PlaylistList
from django.urls import path, include, re_path

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'files', AdminFileViewSet)
router.register(r'playlist-item', AdminPlaylistItemViewSet)

app_name = "admin_api"
urlpatterns = [
    
]

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
urlpatterns += router.urls
