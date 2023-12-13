from django.contrib import messages
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.shortcuts import render
from django.contrib.auth import views

from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView
from .models import *
from .serializers import *
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm as BaseUserChangeForm,
    PasswordChangeForm as BasePasswordChangeForm,
)
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.http import JsonResponse
from django.contrib.auth import (
    REDIRECT_FIELD_NAME,
    get_user_model,
    login as auth_login,
    logout as auth_logout,
    update_session_auth_hash,
)

from rest_framework import viewsets, permissions

from mysite.permissions import *
from django.core import serializers


class UserChangeView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form)

        return JsonResponse({"messages": "Your profile has been updated!"})

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"errors": errors}, status=400)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CustumUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class SignupView(FormView):
    template_name = "signup.html"
    form_class = CustumUserCreationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AccountView(TemplateView):
    template_name = "index.html"


class PasswordChangeForm(BasePasswordChangeForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
        )


class PasswordChangeViewDashboard(views.PasswordChangeView):
    template_name = "password_change.html"
    form_class = PasswordChangeForm

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)

        user = self.request.user
        serialized_user = serializers.serialize(
            "json",
            [
                user,
            ],
        )
        return JsonResponse(serialized_user, safe=False)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({"errors": errors}, status=400)


# from subscriptions.models import *


class ProfileView(TemplateView):
    template_name = "profile.html"
    # def get_context_data(self, **kwargs):
    #     get_context_data = super().get_context_data(**kwargs)
    #     get_context_data.update({'subscriptions': Subscription.objects.filter(user=self.request.user).all()})
    #     return get_context_data


class CoursesView(TemplateView):
    template_name = "courses.html"


class ProgressView(TemplateView):
    template_name = "progress.html"


class PlaylistView(TemplateView):
    template_name = "playlist.html"


class HistoryView(TemplateView):
    template_name = "history.html"


class ScheduleView(TemplateView):
    template_name = "schedule.html"


class SigninView(views.LoginView):
    next_page = "/dashboards"
    template_name = "registration/login.html"


class LoginView(views.LoginView):
    next_page = "/dashboards"
    template_name = "registration/login.html"


class LogoutView(views.LogoutView):
    pass


class PasswordChangeView(views.PasswordChangeView):
    pass


class PasswordChangeDoneView(views.PasswordChangeDoneView):
    pass


class PasswordResetView(views.PasswordResetView):
    pass


class PasswordResetDoneView(views.PasswordResetDoneView):
    pass


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    pass


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    pass


from .serializers import *
from core.api.views import *
from django import forms
from courses.models import Grade
import django_filters


class EnrollmentFilter(django_filters.FilterSet):
    class Meta:
        model = Enrollment
        fields = {
            "grade_id": ["exact"],
            "status": ["exact"],
        }


class EnrollmentViewSet(CoreViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filterset_class = EnrollmentFilter
    filterset_fields = ["grade_id", "status"]
    search_fields = [
        "student__first_name",
        "teacher__last_name",
    ]


class AdminEnrollmentViewSet(AdminCoreViewSet, EnrollmentViewSet):
    pass


from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class InstructorEnrollmentViewSet(InstructorViewSet, EnrollmentViewSet):
    def get_queryset(self):
        qs = super().get_queryset()
        return self.filter_queryset(qs.filter(teacher=self.request.user.teacher))

    def list(self, request, format=None):
        queryset = self.get_queryset()

        if request.accepted_renderer.format == "html":
            data = {
                "object_list": queryset,
                "filter": self.filterset_class(request.GET),
            }

            return Response(data, template_name="instructors/enrollment_list.html")

        serializer = self.serializer_class(queryset, many=True)
        data = serializer.data
        return Response(data)

    def retrieve(self, request, pk=None, format=None):
        queryset = self.get_queryset()
        object = get_object_or_404(queryset, pk=pk)

        if request.accepted_renderer.format == "html":
            data = {"object": object}
            return Response(data, template_name="instructors/enrollment_detail.html")

        serializer = self.serializer_class(object)
        data = serializer.data
        return Response(data)


from core.api.views import *


class AvatarViewSet(CoreViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer


class AdminAvatarViewSet(AdminCoreViewSet, AvatarViewSet):
    pass


class DashboardAvatarViewSet(DashboardCoreViewSet, AvatarViewSet):
    pass

class StudentViewSet(CoreViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class AdminStudentViewSet(AdminCoreViewSet, StudentViewSet):
    pass


class DashboardStudentViewSet(DashboardCoreViewSet, StudentViewSet):
    pass
