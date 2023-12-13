from django import template
register = template.Library()
from django.conf import settings
import mimetypes

@register.simple_tag()
def get_file(obj):
    if obj:
        mime_type, _ = mimetypes.guess_type(obj)
        if mime_type:
            
            if mime_type.startswith('image') :
                return obj
            
            if mime_type == "application/pdf":
                return settings.STATIC_URL + 'core/assets/media/svg/files/pdf.svg'
            
            return settings.MEDIA_URL + 'blank-image.svg'
        
        return settings.STATIC_URL + 'core/assets/media/svg/files/upload.svg'
    else:
        return settings.MEDIA_URL + 'default.png'

# @register.simple_tag()
# def get_file_by_pk(obj):
#     if obj is not None:
#         file = File.objects.filter(pk=obj.value).first()
#         return file.file.url
#     return obj

# @register.simple_tag()
# def get_file_by_value(obj):
#     file = File.objects.filter(pk=obj).first()
#     return file.file.url