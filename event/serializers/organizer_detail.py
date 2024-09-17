from rest_framework import serializers

from event.models import OrganizerEvent


class OrganizerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizerEvent
        fields = ['name', 'site_url', 'phone_number', 'email', 'instagram_url', 'facebook_url', 'telegram_url']
