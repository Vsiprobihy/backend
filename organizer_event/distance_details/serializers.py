from rest_framework import serializers

from organizer_event.additional_items.models import AdditionalItemEvent
from organizer_event.additional_items.serializers import AdditionalItemEventSerializer
from organizer_event.distance_details.models import DistanceEvent
from organizer_event.models import Event


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
            option_data['distance'] = distance
            AdditionalItemEvent.objects.create(**option_data)

        return distance

    def update(self, instance, validated_data):
        additional_options_data = validated_data.pop('additional_options', None)

        instance.name = validated_data.get('name', instance.name)
        instance.competition_type = validated_data.get('competition_type', instance.competition_type)
        instance.category = validated_data.get('category', instance.category)
        instance.length = validated_data.get('length', instance.length)
        instance.start_number_from = validated_data.get('start_number_from', instance.start_number_from)
        instance.start_number_to = validated_data.get('start_number_to', instance.start_number_to)
        instance.age_from = validated_data.get('age_from', instance.age_from)
        instance.age_to = validated_data.get('age_to', instance.age_to)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.is_free = validated_data.get('is_free', instance.is_free)
        instance.promo_only_registration = validated_data.get('promo_only_registration', instance.promo_only_registration)  # noqa: E501
        instance.show_name_on_number = validated_data.get('show_name_on_number', instance.show_name_on_number)
        instance.show_start_number = validated_data.get('show_start_number', instance.show_start_number)
        instance.save()

        if additional_options_data is not None:
            existing_ids = [opt.id for opt in instance.additionalitemevent_set.all()]
            input_ids = [item.get('id') for item in additional_options_data if 'id' in item]

            for opt_id in set(existing_ids) - set(input_ids):
                AdditionalItemEvent.objects.filter(id=opt_id).delete()

            for option_data in additional_options_data:
                option_id = option_data.get('id', None)
                if option_id:
                    option_instance = AdditionalItemEvent.objects.get(id=option_id)
                    for attr, value in option_data.items():
                        setattr(option_instance, attr, value)
                    option_instance.save()
                else:
                    option_data['distance'] = instance
                    AdditionalItemEvent.objects.create(**option_data)

        return instance
