from rest_framework import serializers
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

    def create(self, validated_data):
        event = validated_data.pop('event')
        distance_event = DistanceEvent.objects.create(event=event, **validated_data)
        return distance_event


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = ['event', 'registration_date', 'is_confirmed']
        read_only_fields = ['registration_date', 'is_confirmed']

    def validate_event(self, value):
        """
        Проверка: убедитесь, что событие существует и пользователь может на него зарегистрироваться.
        """
        if not Event.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Event does not exist.")
        return value


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

    # Метод создания события с дополнительными элементами и дистанциями
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

    # Метод обновления события с дополнительными элементами и дистанциями
    def update(self, instance, validated_data):
        organizer_data = validated_data.pop('organizer')
        additional_items_data = validated_data.pop('additional_items')
        distances_data = validated_data.pop('distances')

        organizer, _ = OrganizerEvent.objects.update_or_create(pk=instance.organizer.id, defaults=organizer_data)
        instance.organizer = organizer

        # Обновление дополнительных элементов
        instance.additional_items.all().delete()  # Сначала удаляем все старые элементы
        for item_data in additional_items_data:
            AdditionalItemEvent.objects.create(event=instance, **item_data)

        # Обновление дистанций
        instance.distances.all().delete()  # Сначала удаляем все старые дистанции
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
