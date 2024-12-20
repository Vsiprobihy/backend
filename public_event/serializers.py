from rest_framework import serializers

from event.distance_details.serializers import PublicDistanceEventSerializer
from event.models import Event
from event.serializers import CompetitionTypeSerializer
from organization.models import Organizer
from organization.serializers import OrganizerSerializer


class PublicEventSerializer(serializers.ModelSerializer):
    distances = PublicDistanceEventSerializer(many=True)
    competition_type = CompetitionTypeSerializer(many=True)
    place_region = serializers.CharField(required=True)
    organizer = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['name', 'organizer', 'competition_type', 'date_from', 'date_to',
                  'place_region', 'place', 'photos', 'distances']
        ref_name = 'EventSerializer'

    def get_organizer(self, obj):
        organizer = Organizer.objects.filter(organization=obj.organization).first()
        return OrganizerSerializer(organizer).data if organizer else None
