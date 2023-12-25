from django.urls import path, include, re_path
from .views import *

app_name = "testprep"

urlpatterns = [
    
    path("<uuid:pk>", TestPrepView.as_view(), name="testprep-detail"),
    # path("part/<uuid:pk>", TestPrepPartView.as_view(), name="testprep-part-detail"),
    path("part/<uuid:pk>/questions", TestPrepPartQuestionsView.as_view(), name="testprep-part-questions"),

    
    path("result/<uuid:pk>", TestPrepResultView.as_view(), name="testprep-result-detail"),
    path("result/part/<uuid:pk>", PartResultDetailView.as_view(), name="part-result-detail"),
    
    path("bookmark/create", BookmarkCreateView.as_view(), name="bookmark-create"),
]
