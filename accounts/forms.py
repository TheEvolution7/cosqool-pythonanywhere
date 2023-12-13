from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import *
class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_of_birth', 'email', )
