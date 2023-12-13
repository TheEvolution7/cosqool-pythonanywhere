from rest_framework import serializers
from .models import *


class ReportErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportError
        fields = "__all__"