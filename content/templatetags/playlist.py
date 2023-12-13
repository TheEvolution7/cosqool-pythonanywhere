from django import template
register = template.Library()
from django import forms
from ..models import *
from dashboards.views import PlaylistUpdateDashboardForm
class PlaylistCreateDashboardForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('title', )
        
@register.inclusion_tag('create_playlist_form.html', takes_context=True)
def create_playlist_form(context):
    return {"form": PlaylistUpdateDashboardForm()}