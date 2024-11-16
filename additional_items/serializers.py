from rest_framework import serializers

from additional_items.models import AdditionalItemEvent
from distance_details.models import DistanceEvent


class AdditionalItemEventSerializer(serializers.ModelSerializer):
    distance = serializers.PrimaryKeyRelatedField(queryset=DistanceEvent.objects.all(), required=False)

    class Meta:
        model = AdditionalItemEvent
        fields = ['id', 'item_type', 'price', 'distance']
        extra_kwargs = {
            'id': {'read_only': True}
        }
