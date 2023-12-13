from django.utils.translation import gettext_lazy as _
from .models import *
from core.admin import *
from django.http import JsonResponse
from django.urls import path


class PlaylistItemInline(admin.StackedInline):
    model = PlaylistItem
    extra = 0
    template = "../core/admin/no_stacked_inline.html"
    fields = ('pk', )
    readonly_fields = ('pk', )
    

@admin.register(Playlist)
class PlaylistAdmin(BaseCoreAdmin):
    list_display = [
        "str_tag",
        "status_tag",
        "updated_at",
        "video_count_tag",
        "action_tag",
    ]

    @admin.display(description="status")
    def status_tag(self, obj):
        return status_tag(self, obj)

    search_fields = ["id"]
    base_fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "description",
                )
            },
        ),
    )

    @admin.display(description="Video count")
    def video_count_tag(self, obj):
        return obj.items.count()

    def get_prepopulated_fields(self, request, obj=None):
        return {}

    exclude = (
        "image",
        "media",
    )

    inlines = (PlaylistItemInline,)

    def get_urls(self):
        urls = super().get_urls()

        my_urls = [
            path(
                "file-list/",
                self.admin_site.admin_view(ImageUploadView.as_view()),
                name="file_list",
            ),
            path(
                "file-detail/",
                self.admin_site.admin_view(ImageUploadDetailView.as_view()),
                name="file_detail",
            ),
            path(
                "playlist-video-inline/",
                self.admin_site.admin_view(PlaylistItemInlineView.as_view()),
                name="playlist_video_inline",
            ),
            path(
                "playlist-item-detail/",
                self.admin_site.admin_view(PlayListItemDetailView.as_view()),
                name="playlist_item_detail",
            ),
        ]

        return my_urls + urls


@admin.register(PlaylistItem)
class PlaylistItemAdmin(admin.ModelAdmin):
    search_fields = ["playlist_id"]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.files.serializers import FileSerializer
from core.files.models import File
from content.serializers import *
from rest_framework.renderers import (
    TemplateHTMLRenderer,
    JSONRenderer,
    StaticHTMLRenderer,
    BrowsableAPIRenderer,
    AdminRenderer,
)
from rest_framework import generics


class ImageUploadView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "file_list.html"

    def get(self, request, format=None):
        files = File.objects.all().order_by("-created_at")
        return Response({"files": files})


class ImageUploadDetailView(APIView):
    def post(self, request, format=None):
        params = request.data

        serializer = FileSerializer(data=params)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaylistItemInlineView(generics.ListAPIView):
    serializer_class = PlaylistItemSerializer
    queryset = PlaylistItem.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "./playlist_file_list.html"

    def get_queryset(self):
        queryset = PlaylistItem.objects.all()
        playlist_id = self.request.query_params.get("playlist_id")
        if playlist_id is not None:
            queryset = queryset.filter(playlist=playlist_id).all()
        return queryset

    def get(self, request, format=None):
        object_list = self.get_queryset()
        return Response({"object_list": object_list})


class PlayListItemDetailView(APIView):
    def post(self, request, format=None):
        data_list = []
        files = request.data.getlist("files")
        for file in files:
            data_list.append(
                {"file": file, "playlist": "725fd5dc-638f-46c0-8468-20aae5147785"}
            )

        serializer = PlayListItemListSerializer(data=data_list)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
