from rest_framework import serializers
from .models import *
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}  

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        if not value.strip():  
            raise serializers.ValidationError("Username cannot be empty or just spaces.")
        if value.isdigit():  
            raise serializers.ValidationError("Username cannot be fully numeric.")
        if not re.match(r"^[a-zA-Z0-9_]+$", value):  
            raise serializers.ValidationError("Username can only contain letters, numbers, and underscores.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)