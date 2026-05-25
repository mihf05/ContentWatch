from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields do not match."})
        return attrs

    def create(self, validated_data):
        # Remove confirm_password before creating the user
        validated_data.pop('confirm_password')
        
        # used create_user to properly hash the password
        user = User.objects.create_user(
            username=validated_data['email'].split('@')[0], # Fallback username
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']