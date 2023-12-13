# from django.contrib.auth import views
from django.urls import path, include
from .views import *

from .models import User
from rest_framework import routers, serializers, viewsets


app_name = 'accounts'
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password_change/", PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("singup/", SignupView.as_view(), name="singup"),
    path("", AccountView.as_view(), name="index"),
    path("my-profile", ProfileView.as_view(), name="profile"),
    path("my-courses", CoursesView.as_view(), name="courses"),
    path("my-progress", ProgressView.as_view(), name="progress"),
    path("my-playlist", PlaylistView.as_view(), name="playlist"),
    path("my-history", HistoryView.as_view(), name="history"),
    path("my-schedule", ScheduleView.as_view(), name="schedule"),
    
    path("user-change", UserChangeView.as_view(), name="user_change"),
    path("password-change-dashboard", PasswordChangeViewDashboard.as_view(), name="password_change_dashboard"),
    
    
]
