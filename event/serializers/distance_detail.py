from rest_framework import serializers

from event.models import DistanceEvent


class DistanceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceEvent
        fields = ['id', 'name', 'cost', 'is_free', 'event']
        extra_kwargs = {'event': {'read_only': True}}

    def create(self, validated_data):
        event = validated_data.pop('event')
        distance_event = DistanceEvent.objects.create(event=event, **validated_data)
        return distance_event