from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.widgets import Media
from django.templatetags.static import static
from django.utils.encoding import force_str
from django.utils.functional import Promise
from django.utils.translation import get_language
from js_asset import JS

from .configs import DEFAULT_CONFIG


class CKEditorWidget(forms.Select):    
    @property
    def media(self):
        return Media(
            js=(
                "test.js",
            )
        )
    