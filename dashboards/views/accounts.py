from .base import *
from notification.models import Type

class UserChangeView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form)

        return JsonResponse({'messages': 'Your profile has been updated!'})

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)


class CustumUserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User


class SignupView(FormView):
    template_name = 'signup.html'
    form_class = CustumUserCreationForm
    success_url = reverse_lazy('dashboards:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

from haystack.generic_views import SearchView
class SearchView(LoginRequiredMixin, SearchView):
    template_name = 'pages/dashboards/search.html'
    
    
class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/dashboards/index.html'
    
    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)
        
        get_context_data.update({
            'types': Type.objects.filter(status=True).exclude(pk=3).all().order_by("-pk"),
        })
        return get_context_data

from django.contrib.auth.mixins import PermissionRequiredMixin
class AccountTeacherView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ['accounts.add_address']
    template_name = 'pages/dashboards/index.html'
    
    def get_context_data(self, **kwargs):
        get_context_data = super().get_context_data(**kwargs)
        
        get_context_data.update({
            'types': Type.objects.filter(status=True).exclude(pk=3).all().order_by("-pk"),
        })
        return get_context_data


class PasswordChangeForm(LoginRequiredMixin, PasswordChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_of_birth', 'email', )


class PasswordChangeViewDashboard(views.PasswordChangeView):
    template_name = 'password_change.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)

        user = self.request.user
        serialized_user = serializers.serialize('json', [user, ])
        return JsonResponse(serialized_user, safe=False)

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)