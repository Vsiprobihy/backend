from rest_framework import serializers

from event.distance_details.serializers import PublicDistanceEventSerializer
from event.models import Event
from event.serializers import CompetitionTypeSerializer


class PublicEventSerializer(serializers.ModelSerializer):
    distances = PublicDistanceEventSerializer(many=True)
    competition_type = CompetitionTypeSerializer(many=True)

    class Meta:
        model = Event
        fields = ['name', 'competition_type', 'date_from', 'date_to', 'place_region', 'place', 'photos', 'distances']
        ref_name = 'EventSerializer'

    place_region = serializers.CharField(required=True)
