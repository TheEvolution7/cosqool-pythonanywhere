from rest_framework import serializers
from .models import *


class SubscriptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscription
        fields = "__all__"