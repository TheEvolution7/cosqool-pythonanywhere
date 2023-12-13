from django.urls import path, include, re_path
from .views.instructor import *
app_name = 'instructor'
from django.views import defaults as default_views

urlpatterns = [
    path("", IndexTemplateView.as_view(), name="index"),
    path("profile/", include (
        [
            path("", ProfileTemplateView.as_view(), name="profile"),
        ]
    )),
    path("students/", include (
        [
            path("", StudentListView.as_view(), name="student-list"),
            path("<slug:slug>", StudentDetailView.as_view(), name="student-detail"),
        ]
    )),
    # path("enrollments/", include (
    #     [
    #         path("", EnrollmentListView.as_view(), name="enrollment-list"),
    #         path("<int:pk>", EnrollmentDetailView.as_view(), name="enrollment-detail"),
    #     ]
    # )),
    path("notifications/", include (
        [
            path("", NotificationListView.as_view(), name="notification-list"),
        ]
    )),
    path("courses/", include (
        [
            path("", CourseListView.as_view(), name="course-list"),
        ]
    )),
    
    path('logout/', logout_view, name='logout'),
    
]

from rest_framework.routers import DefaultRouter
from accounts.views import InstructorEnrollmentViewSet
router = DefaultRouter()

router.register(r'enrollments', InstructorEnrollmentViewSet)

urlpatterns += router.urls