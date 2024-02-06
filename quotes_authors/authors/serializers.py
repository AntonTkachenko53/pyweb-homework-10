from rest_framework import serializers
from .models import Author
from django.contrib.auth.models import User


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
