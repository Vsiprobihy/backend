from rest_framework import serializers

from event.models import OrganizerEvent


class OrganizerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizerEvent
        fields = '__all__'
        read_only_fields = ['user'] 