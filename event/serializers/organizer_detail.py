from rest_framework import serializers

from authentication.models import CustomUser
from event.models import OrganizationAccess, OrganizerEvent


class OrganizerEventSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = OrganizerEvent
        fields = '__all__'

    def get_users(self, obj):
        access = OrganizationAccess.objects.filter(organization=obj)
        return [
            {'user': access_item.user.email, 'role': access_item.role}
            for access_item in access
        ]


class OrganizationAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationAccess
        fields = ['user', 'role']

    user = serializers.SlugRelatedField(
        slug_field='email', queryset=CustomUser.objects.all()
    )
