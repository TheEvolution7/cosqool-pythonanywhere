from rest_framework import serializers
from .models import *

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = "__all__"

class PlaylistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistItem
        fields = "__all__"

class PlayListItemListSerializer(serializers.ListSerializer):
    child = PlaylistItemSerializer()

    def create(self, validated_data):
        return PlaylistItem.objects.bulk_create([PlaylistItem(**item) for item in validated_data])

