from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import ValidationError

#from .models import TodoItem
from .models import Post

User = get_user_model()

class TodoItemCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=False)
    title = serializers.CharField(max_length=50)
    content = serializers.CharField(max_length=200)

    def validate(self, data):
        return data


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'