from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm, PasswordChangeForm as BasePasswordChangeForm, UserCreationForm as BaseUserCreationForm
from accounts.models import *
# from quizzes.models import *

class UserChangeForm(BaseUserChangeForm):
    template_name = "user_change_form.html"
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'date_of_birth', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
    
class PasswordChangeForm(BasePasswordChangeForm):
    template_name = "password_change_form.html"
    class Meta:
        model = User
        fields = '__all__'

