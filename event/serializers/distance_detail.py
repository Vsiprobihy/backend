from rest_framework import serializers

from event.models import DistanceEvent, Event, AdditionalItemEvent
from event.serializers.additional_items import AdditionalItemEventSerializer


class DistanceEventSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
    additional_options = AdditionalItemEventSerializer(many=True, required=False)

    class Meta:
        model = DistanceEvent
        fields = [
            'id', 'name', 'competition_type', 'category', 'allow_registration', 
            'length', 'start_number_from', 'start_number_to', 'age_from', 'age_to',
            'cost', 'is_free', 'promo_only_registration', 
            'show_name_on_number', 'show_start_number', 'event', 'additional_options'
        ]
        extra_kwargs = {'event': {'read_only': True}}

    def create(self, validated_data):
        additional_options_data = validated_data.pop('additional_options', [])
        distance = DistanceEvent.objects.create(**validated_data)

        for option_data in additional_options_data:
            option_data['event'] = distance.event
            option_data['distance'] = distance
            AdditionalItemEvent.objects.create(**option_data)

        return distance
