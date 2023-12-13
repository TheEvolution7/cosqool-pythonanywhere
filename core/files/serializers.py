from rest_framework import serializers
from .models import File

class FileListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        books = [File(**item) for item in validated_data]
        return File.objects.bulk_create(books)
        
class FileSerializer(serializers.ModelSerializer):
    
    class Meta:
        list_serializer_class = FileListSerializer
        model = File
        fields = '__all__'
        
