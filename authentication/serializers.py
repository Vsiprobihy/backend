import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.models import AdditionalProfile, CustomUser
from django.contrib.auth import get_user_model


def validate_password_confirm(password, password2):
    if password != password2:
        raise serializers.ValidationError("Passwords must match")
    return True


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'password2']

    @staticmethod
    def validate_password(value):
        """
        Ensure that the password contains at least:
        - 1 uppercase letter
        - 1 special character
        - 1 number
        """
        if not re.search(r'[A-Z]', value):
            raise ValidationError("Password must contain at least 1 uppercase letter.")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError("Password must contain at least 1 special character.")

        if not re.search(r'\d', value):
            raise ValidationError("Password must contain at least 1 number.")

        return value

    def validate(self, data):
        validate_password_confirm(data['password'], data['password2'])
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = get_user_model().objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    registered_events = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'gender', 'date_of_birth', 't_shirt_size',
            'country', 'city', 'phone_number', 'sports_club', 'emergency_contact_name',
            'emergency_contact_phone', 'registered_events', 'avatar'
        ]

    def get_registered_events(self, obj):
        from event.serializers.events import EventSerializer
        events = obj.events_registered.all()
        return EventSerializer(events, many=True).data

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

class UserAvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['avatar']

class AdditionalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalProfile
        fields = ['id', 'email', 'first_name', 'last_name']

class AdditionalProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalProfile
        fields = ['id', 'email', 'first_name', 'last_name']
