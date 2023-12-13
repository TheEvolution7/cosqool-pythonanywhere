from .models import *

from rest_framework import serializers
class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer
    class Meta:
        model = Student
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer
    class Meta:
        model = User
        fields = '__all__'
        
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'