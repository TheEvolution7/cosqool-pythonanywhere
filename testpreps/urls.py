from django.urls import path, include, re_path
from .views import *

app_name = "testpreps"

urlpatterns = [
    path("", TestPrepListView.as_view(), name="testprep-list"),
    path("<uuid:pk>", TestPrepDetailView.as_view(), name="testprep-detail"),
    path(
        "testprep-item/<uuid:pk>",
        TestPrepItemDetailView.as_view(),
        name="testprep-item-detail",
    ),
    path(
        "breake/<uuid:pk>",
        BreakeDetailView.as_view(),
        name="breake-detail",
    ),
    path(
        "sections/<uuid:pk>",
        SectionDetailView.as_view(),
        name="section-detail",
    ),
    path(
        "part/<uuid:pk>",
        TestPrepPartView.as_view(),
        name="part-detail",
    ),
    path(
        "part/<uuid:pk>/questions",
        TestPrepPartQuestionsView.as_view(),
        name="testprep-part-questions",
    ),
    path(
        "testprep-results/<uuid:pk>",
        TestPrepResultDetailView.as_view(),
        name="testprep-result-detail",
    ),
    path(
        "section-results/<uuid:pk>",
        SectionResultDetailView.as_view(),
        name="section-result-detail",
    ),
    path(
        "breake-results/<uuid:pk>",
        BreakeResultDetailView.as_view(),
        name="breake-result-detail",
    ),
    # path(
    #     "result/part/<uuid:pk>",
    #     PartResultDetailView.as_view(),
    #     name="part-result-detail",
    # ),
]
