from django.urls import path, include, re_path
from .views import *

app_name = 'courses'
urlpatterns = [
    path("", CoursesView.as_view(), name="list"),
    # path("<slug:slug>/<int:pk>", CourseDetailView.as_view(), name="course-detail"),
    path("videos/<int:pk>", VideoView.as_view(), name="video-detail"),
    
    path("testprep/<int:pk>", TestPrepView.as_view(), name="testprep-detail"),
    path("testprep/result/<int:pk>", TestPrepResultView.as_view(), name="testprep-result"),
    
    re_path(r'^(?P<slug>[\u0600-\u06FF\w-]+)/$', CourseDetailView.as_view(), name='course-detail'),
    
    path("<slug:slug>/<int:pk>", CourseDetailVideoView.as_view(), name="course-detail-video"),

    
    
]
