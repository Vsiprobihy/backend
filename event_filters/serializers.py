from rest_framework import serializers

from event.models import CompetitionType, DistanceEvent, Event


class DistanceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceEvent
        fields = ['name']
        ref_name = 'DistanceSerializer'


class CompetitionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionType
        fields = ['name']


class EventSerializer(serializers.ModelSerializer):
    distances = DistanceEventSerializer(many=True)
    competition_type = CompetitionTypeSerializer(many=True)

    class Meta:
        model = Event
        fields = ['name', 'competition_type', 'date_from', 'date_to', 'place_region', 'place', 'photos', 'distances']
        ref_name = 'EventSerializer'

    place_region = serializers.CharField(required=True)
