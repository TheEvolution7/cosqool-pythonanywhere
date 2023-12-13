from django.contrib.auth import views
from accounts.models import *
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy


class LoginView(views.LoginView):
    next_page = '/dashboards'
    template_name = 'registration/login.html'


class SigninView(views.LoginView):
    next_page = '/dashboards'
    template_name = 'registration/login.html'


class CustumUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class SignupView(FormView):
    template_name = 'signup.html'
    form_class = CustumUserCreationForm
    success_url = reverse_lazy('auth:signin')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


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
