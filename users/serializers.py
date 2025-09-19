from rest_framework import serializers

from users.models import Client


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Client
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Client.objects.create_user(password=password, **validated_data)
        return user


class ActivateSerializer(serializers.Serializer):
    code = serializers.UUIDField()
