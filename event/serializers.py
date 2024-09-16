from rest_framework import serializers

from authentication.serializers import UserProfileSerializer
from .models import EventRegistration, Event, OrganizerEvent, AdditionalItemEvent, DistanceEvent


class OrganizerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizerEvent
        fields = ['name', 'site_url', 'phone_number', 'email', 'instagram_url', 'facebook_url', 'telegram_url']


class AdditionalItemEventSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)

    class Meta:
        model = AdditionalItemEvent
        fields = ['id', 'item_type', 'price', 'event']
        extra_kwargs = {'event': {'read_only': True}}


class DistanceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceEvent
        fields = ['name', 'cost', 'is_free', 'event']
        extra_kwargs = {'event': {'read_only': True}}

    def create(self, validated_data):
        event = validated_data.pop('event')
        distance_event = DistanceEvent.objects.create(event=event, **validated_data)
        return distance_event


class EventRegistrationSerializer(serializers.ModelSerializer):
    distances = serializers.PrimaryKeyRelatedField(queryset=DistanceEvent.objects.all(), many=True)
    additional_items = serializers.PrimaryKeyRelatedField(queryset=AdditionalItemEvent.objects.all(), many=True)

    class Meta:
        model = EventRegistration
        fields = ['event', 'distances', 'additional_items', 'registration_date', 'is_confirmed']
        read_only_fields = ['registration_date', 'is_confirmed']

    def validate(self, data):
        if not data.get('distances'):
            raise serializers.ValidationError("At least one distance must be selected.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        event = validated_data['event']
        additional_items_data = validated_data.pop('additional_items', [])
        distances_data = validated_data.pop('distances', [])

        print("Received additional_items:", additional_items_data)
        print("Received distances:", distances_data)

        registration = EventRegistration.objects.create(user=user, event=event)

        registration.distances.set(distances_data)

        if additional_items_data:
            print("Setting additional_items:", additional_items_data)
            registration.additional_items.set(additional_items_data)
        else:
            print("No additional items to set.")

        registration.save()
        return registration

class EventRegistrationDetailSerializer(serializers.ModelSerializer):
    distances = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=DistanceEvent.objects.all()
    )
    additional_items = serializers.SlugRelatedField(
        many=True,
        slug_field='item_type',
        queryset=AdditionalItemEvent.objects.all()
    )

    class Meta:
        model = EventRegistration
        fields = ['event', 'distances', 'additional_items', 'registration_date', 'is_confirmed']




class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerEventSerializer()
    additional_items = AdditionalItemEventSerializer(many=True)
    distances = DistanceEventSerializer(many=True)

    class Meta:
        model = Event
        fields = ['name', 'competition_type', 'date_from', 'date_to', 'place', 'photos', 'description',
                  'registration_link',
                  'hide_participants', 'schedule_pdf', 'organizer', 'additional_items', 'distances',
                  'extended_description']

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
        organizer_data = validated_data.pop('organizer')
        additional_items_data = validated_data.pop('additional_items')
        distances_data = validated_data.pop('distances')

        organizer, _ = OrganizerEvent.objects.update_or_create(pk=instance.organizer.id, defaults=organizer_data)
        instance.organizer = organizer

        instance.additional_items.all().delete()
        for item_data in additional_items_data:
            AdditionalItemEvent.objects.create(event=instance, **item_data)

        instance.distances.all().delete()
        for distance_data in distances_data:
            DistanceEvent.objects.create(event=instance, **distance_data)

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

        instance.save()

        return instance
