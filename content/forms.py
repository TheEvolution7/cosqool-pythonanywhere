from dal import autocomplete
from dal_select2.fields import Select2ListChoiceField
from dal_select2.views import Select2ListView
from dal_select2.widgets import ListSelect2
from django import forms

from .models import Playlist

class CountryAutocompleteFromList(Select2ListView):
    def get_list(self):
        return ['France', 'Fiji', 'Finland', 'Switzerland']
def get_choice_list():
    return [model.test for model in Playlist.objects.all()]


def get_choice_list_with_id():
    return [[str(model.id), model.test] for model in Playlist.objects.all()]


class PlaylistForm(forms.ModelForm):
    test = Select2ListChoiceField(
        choice_list=get_choice_list,
        required=False,
        widget=ListSelect2(url='country-list-autocomplete')
    )