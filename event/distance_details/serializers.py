from rest_framework import serializers

from event.additional_items.models import AdditionalItemEvent
from event.additional_items.serializers import AdditionalItemEventSerializer
from event.distance_details.models import DistanceEvent
from event.models import Event


class DistanceEventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
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
            option_data['distance'] = distance
            AdditionalItemEvent.objects.create(**option_data)

        return distance

    def update(self, instance, validated_data):
        additional_options_data = validated_data.pop('additional_options', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if additional_options_data is not None:
            existing_ids = [opt.id for opt in instance.additional_options.all()]
            input_ids = [item.get('id') for item in additional_options_data if 'id' in item]

            for opt_id in set(existing_ids) - set(input_ids):
                AdditionalItemEvent.objects.filter(id=opt_id).delete()

            for option_data in additional_options_data:
                option_id = option_data.get('id', None)
                if option_id:
                    try:
                        # Try to fetch the existing additional item by ID and update it
                        option_instance = AdditionalItemEvent.objects.get(id=option_id, distance=instance)
                        for attr, value in option_data.items():
                            setattr(option_instance, attr, value)
                        option_instance.save()
                    except AdditionalItemEvent.DoesNotExist:
                        option_data['distance'] = instance
                        AdditionalItemEvent.objects.create(**option_data)
                else:
                    option_data['distance'] = instance
                    AdditionalItemEvent.objects.create(**option_data)

        return instance

class PublicDistanceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceEvent
        fields = ['name']
