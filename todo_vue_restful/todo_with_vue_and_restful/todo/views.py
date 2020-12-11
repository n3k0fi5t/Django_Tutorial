import json

from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import PostSerializer

# Create your views here.
class PostsView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            obj = Post.objects.create(**serializer.validated_data)
            return Response(serializer.validated_data)
        else:
            return Response(status=400)