from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Client


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Client
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Client.objects.create_user(password=password, **validated_data)
        return user


class ActivateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.UUIDField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)