from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _

from core.admin import *
from django.template.response import TemplateResponse
from django.http import HttpResponse, JsonResponse
from django.urls import path

from django.contrib.admin.options import InlineModelAdmin
class CustomInline(InlineModelAdmin):
    template = 'albums/admin/edit_inline/upload.html'
    
class ImageAdminInline(TranslatableStackedInline):
    model = Image
    template = 'albums/admin/edit_inline/upload.html'
    extra = 0
    fields = ('image_preview', )
    readonly_fields = ('image_preview', )
    
    
    
@admin.register(Gallery)
class GalleryAdmin(CoreAdmin):
    inlines = (ImageAdminInline, )

    
    @admin.display(description='Images Count')
    def images_count(self, obj):
        return obj.gallery_images.count()

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path('<path:object_id>/change/bulk-upload/',
                 self.admin_site.admin_view(self.bulk_upload), name='albums_gallery_uploads'),

            path('<path:object_id>/change/upload/',
                 self.admin_site.admin_view(self.upload, cacheable=True)),
        ]

        return my_urls + urls
    
    def upload(self, request, object_id):
        context = dict(
            self.admin_site.each_context(request),
            items=Image.objects.filter(gallery__in=object_id).all(),
            object_id=object_id
        )

        return TemplateResponse(request, "albums/upload.html", context)

    def bulk_upload(self, request, object_id):
        if request.method == 'POST':
            my_file = request.FILES.get('image')
            gallery = Gallery.objects.filter(pk=object_id).first()
            Image.objects.create(title=gallery, gallery_id=object_id, image=my_file)
            return HttpResponse('1')
        return JsonResponse({'post': 'fasle'})

    def get_link(super):
        return super

@admin.register(Image)
class ImageAdmin(CoreAdmin):
    pass
    
@admin.register(Group)
class GroupAdmin(CoreCategoryAdmin):
    pass
