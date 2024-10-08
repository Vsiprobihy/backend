from rest_framework import serializers

from event.models import DistanceEvent
from event.models import Event

class DistanceEventSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
    
    class Meta:
        model = DistanceEvent
        fields = ['id', 'name', 'cost', 'is_free', 'event']
        extra_kwargs = {'event': {'read_only': True}}
