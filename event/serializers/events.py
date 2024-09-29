from rest_framework import serializers

from .additional_items import AdditionalItemEventSerializer
from .distance_detail import DistanceEventSerializer
from .organizer_detail import OrganizerEventSerializer
from ..models import Event, OrganizerEvent, AdditionalItemEvent, DistanceEvent


class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerEventSerializer(required=False)
    additional_items = AdditionalItemEventSerializer(many=True, required=False)
    distances = DistanceEventSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ['name', 'competition_type', 'date_from', 'date_to', 'place', 'photos', 'description',
                  'registration_link', 'hide_participants', 'schedule_pdf', 'organizer', 'additional_items',
                  'distances', 'extended_description']

    def __init__(self, *args, **kwargs):
        # Перевіряємо контекст на наявність методу запиту
        super().__init__(*args, **kwargs)
        request_method = self.context['request'].method if 'request' in self.context else None

        # Якщо це POST-запит, робимо поля обов'язковими
        if request_method == 'POST':
            self.fields['organizer'].required = True
            self.fields['additional_items'].required = True
            self.fields['distances'].required = True
        else:
            # Якщо PUT або PATCH, ці поля не обов'язкові
            self.fields['organizer'].required = False
            self.fields['additional_items'].required = False
            self.fields['distances'].required = False

    def create(self, validated_data):
        organizer_data = validated_data.pop('organizer')
        additional_items_data = validated_data.pop('additional_items')
        distances_data = validated_data.pop('distances')

        organizer, _ = OrganizerEvent.objects.get_or_create(**organizer_data)
        event = Event.objects.create(organizer=organizer, **validated_data)

        for item_data in additional_items_data:
            AdditionalItemEvent.objects.create(event=event, **item_data)

        for distance_data in distances_data:
            DistanceEvent.objects.create(event=event, **distance_data)

        return event

    def update(self, instance, validated_data):
        # Ігноруємо поля additional_items, distances і organizer під час оновлення
        validated_data.pop('organizer', None)
        validated_data.pop('additional_items', None)
        validated_data.pop('distances', None)

        instance.name = validated_data.get('name', instance.name)
        instance.competition_type = validated_data.get('competition_type', instance.competition_type)
        instance.date_from = validated_data.get('date_from', instance.date_from)
        instance.date_to = validated_data.get('date_to', instance.date_to)
        instance.place = validated_data.get('place', instance.place)
        instance.photos = validated_data.get('photos', instance.photos)
        instance.description = validated_data.get('description', instance.description)
        instance.registration_link = validated_data.get('registration_link', instance.registration_link)
        instance.hide_participants = validated_data.get('hide_participants', instance.hide_participants)
        instance.schedule_pdf = validated_data.get('schedule_pdf', instance.schedule_pdf)
        instance.extended_description = validated_data.get('extended_description', instance.extended_description)

        instance.save()

        return instance
