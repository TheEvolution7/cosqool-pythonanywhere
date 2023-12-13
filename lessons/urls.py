from django.urls import path, include, re_path
from .views import *

app_name = 'lessons'
urlpatterns = [
    re_path(r'^(?P<slug>[\u0600-\u06FF\w-]+)/$', SectionItemDetailView.as_view(), name='section-item-detail'),
    path("learn/<slug:slug>/", LearnDetailView.as_view(), name="learn-detail"),
]
