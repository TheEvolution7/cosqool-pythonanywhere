from django.conf import settings
from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter, SimpleRouter

from .api.views import FileViewSet

router = DefaultRouter()

router.register(r'files', FileViewSet)

app_name = "api_files"
urlpatterns = [
]
urlpatterns += router.urls

