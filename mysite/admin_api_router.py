from django.conf import settings
from django.urls import path, include, re_path

from rest_framework import routers

from core.files.api.views import AdminFileViewSet

router = routers.DefaultRouter()

router.register('files/', AdminFileViewSet)

urlpatterns = [
]
urlpatterns += router.urls
