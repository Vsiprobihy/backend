from rest_framework import serializers

from event.models import (
    AdditionalItemEvent,
    CompetitionType,
    DistanceEvent,
    Event,
    OrganizationAccess,
    OrganizerEvent,
)
from event.serializers.distance_detail import DistanceEventSerializer
from event.serializers.organizer_detail import OrganizerEventSerializer


class CompetitionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionType
        fields = ['name']


class EventSerializer(serializers.ModelSerializer):
    organizer_id = serializers.IntegerField(write_only=True)
    organizer = OrganizerEventSerializer(read_only=True)
    distances = DistanceEventSerializer(many=True, required=True)
    competition_type = CompetitionTypeSerializer(many=True)

    class Meta:
        model = Event
        fields = [
            'name', 'competition_type', 'date_from', 'date_to', 'place', 'place_region',
            'photos', 'description', 'registration_link', 'hide_participants', 'schedule_pdf',
            'organizer', 'organizer_id', 'distances', 'extended_description'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['competition_type'].required = True
        self.fields['date_from'].required = True
        self.fields['date_to'].required = True
        self.fields['place'].required = True
        self.fields['place_region'].required = True
        self.fields['description'].required = False
        self.fields['registration_link'].required = False
        self.fields['hide_participants'].required = False
        self.fields['schedule_pdf'].required = False
        self.fields['extended_description'].required = False

    def validate(self, data):
        instance_date_from = getattr(self.instance, 'date_from', None)
        instance_date_to = getattr(self.instance, 'date_to', None)

        date_from = data.get('date_from', instance_date_from)
        date_to = data.get('date_to', instance_date_to)

        if date_from and date_to:
            if date_to < date_from:
                raise serializers.ValidationError({
                    'date_to': 'The end date cannot be earlier than the start date.',
                    'date_from': 'The start date cannot be later than the end date.'
                })

        return data

    def create(self, validated_data):
        organizer_id = validated_data.pop('organizer_id')
        distances_data = validated_data.pop('distances')
        competition_type_data = validated_data.pop('competition_type', [])

        user = self.context['request'].user

        if not OrganizationAccess.objects.filter(organization_id=organizer_id, user=user).exists():
            raise serializers.ValidationError({'organizer_id': 'You do not have access to the specified organization.'})

        try:
            organizer = OrganizerEvent.objects.get(id=organizer_id)
        except OrganizerEvent.DoesNotExist:
            raise serializers.ValidationError(
                {
                    'organizer_id': 'The organization with the specified ID was not found.'
                }
            )

        event = Event.objects.create(organizer=organizer, **validated_data)

        for comp in competition_type_data:
            competition_type_obj = CompetitionType.objects.filter(
                name=comp['name']
            ).first()
            if competition_type_obj:
                event.competition_type.add(competition_type_obj)
            else:
                raise serializers.ValidationError(
                    {
                        'competition_type': f"Competition type '{comp['name']}' does not exist."
                    }
                )

        for distance_data in distances_data:
            additional_options_data = distance_data.pop('additional_options', [])
            distance = DistanceEvent.objects.create(event=event, **distance_data)

            for option_data in additional_options_data:
                option_data['distance'] = distance
                AdditionalItemEvent.objects.create(**option_data)

        return event

    def update(self, instance, validated_data):
        validated_data.pop('organizer', None)
        competition_type_data = validated_data.pop('competition_type', None)

        user = self.context['request'].user
        organizer_id = validated_data.get('organizer_id', instance.organizer.id)

        if not OrganizationAccess.objects.filter(organization_id=organizer_id, user=user).exists():
            raise serializers.ValidationError({'organizer_id': 'You do not have access to the specified organization.'})

        if competition_type_data is not None:
            instance.competition_type.clear()
            for comp in competition_type_data:
                competition_type_obj = CompetitionType.objects.filter(
                    name=comp['name']
                ).first()
                if competition_type_obj:
                    instance.competition_type.add(competition_type_obj)
                else:
                    raise serializers.ValidationError(
                        {
                            'competition_type': f"Competition type '{comp['name']}' does not exist."
                        }
                    )

        instance.name = validated_data.get('name', instance.name)
        instance.date_from = validated_data.get('date_from', instance.date_from)
        instance.date_to = validated_data.get('date_to', instance.date_to)
        instance.place = validated_data.get('place', instance.place)
        instance.place_region = validated_data.get(
            'place_region', instance.place_region
        )
        instance.photos = validated_data.get('photos', instance.photos)
        instance.description = validated_data.get('description', instance.description)
        instance.registration_link = validated_data.get(
            'registration_link', instance.registration_link
        )
        instance.hide_participants = validated_data.get(
            'hide_participants', instance.hide_participants
        )
        instance.schedule_pdf = validated_data.get(
            'schedule_pdf', instance.schedule_pdf
        )
        instance.extended_description = validated_data.get(
            'extended_description', instance.extended_description
        )

        instance.save()
        return instance
