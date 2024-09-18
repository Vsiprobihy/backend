from rest_framework import serializers

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    registered_events = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'gender', 'date_of_birth', 't_shirt_size',
            'country', 'city', 'phone_number', 'sports_club', 'emergency_contact_name',
            'emergency_contact_phone', 'registered_events'
        ]

    def get_registered_events(self, obj):
        from event.serializers.events import EventSerializer
        events = obj.events_registered.all()
        return EventSerializer(events, many=True).data
