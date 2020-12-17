from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import TodoItem

class TodoItemCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    content = serializers.CharField(required=False)


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ['title', 'content', 'is_finished', 'finish_time', 'id']


class TodoItemEditSerializer(TodoItemCreateSerializer):
    is_finished = serializers.BooleanField()