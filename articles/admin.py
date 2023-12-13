from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _

from core.admin import *

import facebook
from django.urls import path
from django.http import HttpResponseRedirect
    
def action_tag(self, obj):
    return mark_safe(f'<div class="sweetalert"><div class="d-flex justify-content-end"><a href="{obj.id}/share" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1" title="Share"><i class="fa fa-share"></i></a><a href="{obj.id}/change" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1" title="Edit"><i class="fa fa-pencil"></i></a><a href="{obj.id}/delete" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1" title="Delete"><i class="fa fa-trash"></i></a></div></div>')

def share_on_facebook(content, access_token):
    graph = facebook.GraphAPI(access_token)
    graph.put_object(parent_object='me', connection_name='feed', message=content)
    
@admin.register(Article)
class ArticleAdmin(CoreAdmin):
    
    
    @admin.display(description='action')
    def action_tag(self, obj):
        return action_tag(self, obj)
    
    list_display = ['str_tag', 'author_tag', 'categories_tag', 'action_tag']
    
    @admin.display(description='Categories')
    def categories_tag(self, obj):
        html = '<div class="min-w-150px">'
        for category in obj.get_category_list():
            url = reverse('admin:articles_articlecategory_change', args=[category.id])
            html += f'<a target="_blank" href="{url}" class="badge badge-light-primary fs-7 m-1">{category}</a>'
        
        html += '</div>'
        return mark_safe(html)
    
    # @admin.display(description='Tags')
    # def tags_tag(self, obj):
    #     html = '<div class="min-w-150px">'
    #     for tag in obj.get_tags():
    #         url = reverse('admin:articles_tag_change', args=[tag.id])
    #         html += f'<a target="_blank" href="{url}" class="badge badge-light-primary fs-7 m-1">{tag}</a>'
    #     html += '</div>'
    #     return mark_safe(html)
    
    @admin.display(description='Author')
    def author_tag(self, obj):
        url = reverse('admin:accounts_user_change', args=[obj.author.id])
        return mark_safe(f'<a target="_blank" href="{url}" class="badge badge-light-primary fs-7 m-1">{obj.author}</a>')
    
    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path('<path:object_id>/share/',
                 self.admin_site.admin_view(self.share, cacheable=True)),
        ]

        return my_urls + urls
    
    def share(self,request,object_id):
        obj = Article.objects.filter(pk=object_id).first()
        access_token = 'EAAIGu5Eeej0BAERh8whfGUii3NNIrwcIMuju3yrWtxbBuYrO5J9vvUluZBxdS5CysDZAs76ZCxqrthiWLrjxKuZBJSDRoZAIBgjaiFdDAejf1FXtq5EbZCf74CklVJZCQJp28APd9AnhFOeBDY28mniXe199Qrl9zNqwI5pDkZAdVwZDZD'
        content = f"New post published: {obj.title}"
        share_on_facebook(content, access_token)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@admin.register(ArticleCategory)
class ArticleCategoryAdmin(BaseCoreAdmin, MPTTModelAdmin, ImportExportModelAdmin, ExportActionModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(CoreAdmin):
    list_display = ['str_tag', 'slug', 'articles_tag', 'action_tag']
    
    @admin.display(description='Count')
    def articles_tag(self, obj):
        return obj.articles().count()
