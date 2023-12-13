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
        