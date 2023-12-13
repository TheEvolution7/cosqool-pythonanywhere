from rest_framework.views import APIView
from reporterror.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

class ReportErrorCreateAPIView(generics.ListCreateAPIView):
    queryset = ReportError.objects.all()
    serializer_class = ReportErrorSerializer
    model = ReportError
     
    def get(self, request, format=None):
        snippets = ReportError.objects.all()
        serializer = ReportErrorSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        params = request.data
        user = request.user
        params.update(user=user.pk)
        serializer = ReportErrorSerializer(data=params)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)