from .base import *
from notes.models import *
from notes.serializer import *

from django.core import serializers
from rest_framework.views import APIView
from rest_framework import generics
from testpreps.serializers import *
from rest_framework.response import Response
from rest_framework import status

from rest_framework import mixins
from rest_framework import generics

class NoteAPIView(APIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    model = Note

    def post(self, request, *args, **kwargs):
        params = request.data
        user = request.user
        params.update(user=user.pk)

        serializer = NoteSerializer(data=params)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteUpdateAPIView(generics.UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    model = Note

    def put(self, request, pk, format=None):
        params = request.data
        object = self.get_object()
        user = request.user
        params.update(user=user.pk)
        params.update(learn=object.learn.pk)
        serializer = NoteSerializer(object, data=params)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDestroyAPIView(generics.DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    model = Note

    def delete(self, request, pk, format=None):
        object = self.get_object()
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


