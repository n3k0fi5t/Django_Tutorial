from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=6)
    email = serializers.EmailField()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=6)
