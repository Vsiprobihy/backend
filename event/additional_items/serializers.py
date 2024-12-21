from rest_framework import serializers

from event.additional_items.models import AdditionalItemEvent
from event.distance_details.models import DistanceEvent


class AdditionalItemEventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    distance = serializers.PrimaryKeyRelatedField(queryset=DistanceEvent.objects.all(), required=False)

    class Meta:
        model = AdditionalItemEvent
        fields = ['id', 'itemType', 'price', 'distance']
        extra_kwargs = {
            'id': {'read_only': True}
        }
