from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
class ImagePickerWidget(forms.Select): 
    template_name = "./imagepickers.html"
    
    @property
    def is_hidden(self):
        return True
    
    class Media:
        css = {
            "all": [],
        }
        js = ["core/assets/plugins/global/plugins.bundle.js"]
        
class ImagePickerMultipleWidget(forms.SelectMultiple): 
    template_name = "imagepickers.html"
    option_template_name = 'select_option_imagepickers.html'
    
    @property
    def is_hidden(self):
        return True
    
    class Media:
        css = {
            "all": ["image-picker.css"],
        }
        js = ["imagepicker.js", "image-picker.min.js"]


    