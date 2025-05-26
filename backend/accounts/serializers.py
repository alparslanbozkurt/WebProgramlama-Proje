from rest_framework import serializers
from .services.auth_service import AuthService

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return AuthService.register_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = AuthService.verify_credentials(
            username=data['username'],
            password=data['password']
        )
        return {'user_id': user.id, 'username': user.username}