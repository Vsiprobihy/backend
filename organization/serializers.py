import re

from rest_framework import serializers

from authentication.models import CustomUser
from organization.models import Organization, Organizer


class OrganizationSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    phoneNumbers = serializers.ListField(
        child=serializers.CharField(max_length=20),
        allow_empty=True,
        required=False
    )

    class Meta:
        model = Organization
        fields = '__all__'

    def get_mainImage(self, obj):
        request = self.context.get('request')
        if obj.mainImage and request:
            return request.build_absolute_uri(obj.mainImage.url)
        return None

    def get_backgroundImage(self, obj):
        request = self.context.get('request')
        if obj.backgroundImage and request:
            return request.build_absolute_uri(obj.backgroundImage.url)
        return None

    def validate_phone_numbers(self, value):  # noqa
        phone_pattern = re.compile(
            r'^\+380\d{9}$|^\+38\(\d{3}\)\d{7}$|^\+38\(\d{3}\)\d{3}-\d{2}-\d{2}$'
        )
        for phone in value:
            if not phone_pattern.match(phone):
                raise serializers.ValidationError(f'Invalid phone number: {phone}')
        return value

    def get_users(self, obj):  # noqa
        access = Organizer.objects.filter(organization=obj)
        return [
            {'user': access_item.user.email,
             'role': access_item.user.role,
             }
            for access_item in access
        ]


class OrganizerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email', queryset=CustomUser.objects.all()
    )
    organization = serializers.SlugRelatedField(
        slug_field='name', queryset=Organization.objects.all()
    )

    class Meta:
        model = Organizer
        fields = ['user', 'organization']


