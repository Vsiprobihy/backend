from rest_framework import serializers

from authentication.models import CustomUser
from organization.models import Organization, Organizer


class OrganizationSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = '__all__'

    def get_users(self, obj):
        access = Organization.objects.filter(organization=obj)
        return [
            {'user': access_item.user.email, 'role': access_item.role}
            for access_item in access
        ]


class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = ['user', 'role']

    user = serializers.SlugRelatedField(
        slug_field='email', queryset=CustomUser.objects.all()
    )
