from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = 'playlist'

router = routers.SimpleRouter()
router.register(r"", PlaylistViewSet,basename="playlist")

urlpatterns = [
    # path("", include(router.urls, 'app_name')),
    path('', include((router.urls, 'playlist'), namespace='playlist')),
]
