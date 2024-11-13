from rest_framework import serializers

from event.models import AdditionalItemEvent, DistanceEvent, Event


class AdditionalItemEventSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
    distance = serializers.PrimaryKeyRelatedField(queryset=DistanceEvent.objects.all(), required=False)


    class Meta:
        model = AdditionalItemEvent
        fields = ['id', 'item_type', 'price', 'event', 'distance']
        extra_kwargs = {
            'event': {'read_only': True},
            'id': {'read_only': True}
            }
