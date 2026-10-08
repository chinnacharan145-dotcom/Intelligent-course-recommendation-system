from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.students.models import StudentProfile

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        role = validated_data.get('role', User.Role.STUDENT)
        username = validated_data.get('username') or validated_data['email'].split('@')[0]

        user = User.objects.create_user(
            email=validated_data['email'],
            username=username,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=role,
            password=validated_data['password']
        )

        if role == User.Role.STUDENT:
            StudentProfile.objects.get_or_create(user=user)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'phone', 'bio', 'profile_picture', 'is_verified', 'date_joined']
        read_only_fields = ['id', 'email', 'role', 'date_joined']
