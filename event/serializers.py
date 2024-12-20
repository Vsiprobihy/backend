from rest_framework import serializers

from event.additional_items.models import AdditionalItemEvent
from event.age_category.models import AgeCategory
from event.distance_details.models import CostChangeRule, DistanceEvent
from event.distance_details.serializers import DistanceEventSerializer
from event.models import (
    CompetitionType,
    Event,
)
from event.promo_code.models import PromoCode
from organization.models import Organization, Organizer
from organization.serializers import OrganizerSerializer
from utils.constants.constants_event import STATUS_CHOICES


class CompetitionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionType
        fields = ['id', 'name']


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    organization_id = serializers.IntegerField(write_only=True)
    distances = DistanceEventSerializer(many=True, required=True)
    competition_type = CompetitionTypeSerializer(many=True)
    organizer = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'organizer', 'organization_id', 'competition_type', 'date_from', 'date_to',
            'place', 'place_region',
            'photos', 'description', 'registration_link', 'hide_participants', 'schedule_pdf',
            'co_organizer', 'distances', 'extended_description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is None:
            self.fields['distances'].required = True
        else:
            self.fields['distances'].required = False

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
        self.fields['co_organizer'].required = False

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
        organization_id = validated_data.pop('organization_id')
        distances_data = validated_data.pop('distances')
        competition_type_data = validated_data.pop('competition_type', [])

        user = self.context['request'].user

        if not Organizer.objects.filter(organization_id=organization_id, user=user).exists():
            raise serializers.ValidationError({'organization_id': 'You do not have access to the specified '
                                                                  'organization.'})

        try:
            organization = Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            raise serializers.ValidationError({'organization_id': 'The organization with the specified ID was not '
                                                                  'found.'})

        event = Event.objects.create(organization=organization, **validated_data)

        competition_types = []
        for comp in competition_type_data:
            competition_type = CompetitionType.objects.get(name=comp['name'])
            competition_types.append(competition_type)

        event.competition_type.set(competition_types)

        for distance_data in distances_data:
            additional_options_data = distance_data.pop('additional_options', [])
            cost_change_rules_data = distance_data.pop('cost_change_rules', [])
            age_categories_data = distance_data.pop('age_categories', [])
            promo_codes_data = distance_data.pop('promo_codes', [])

            distance = DistanceEvent.objects.create(event=event, **distance_data)

            for option_data in additional_options_data:
                option_data['distance'] = distance
                AdditionalItemEvent.objects.create(**option_data)

            for rule_data in cost_change_rules_data:
                rule_data['distance'] = distance
                CostChangeRule.objects.create(**rule_data)

            for category_data in age_categories_data:
                category_data['distance'] = distance
                AgeCategory.objects.create(**category_data)

            for promo_code_data in promo_codes_data:
                promo_code_data['distance'] = distance
                PromoCode.objects.create(**promo_code_data)

        return event

    def update(self, instance, validated_data):
        distances_data = validated_data.pop('distances', None)
        competition_type_data = validated_data.pop('competition_type', [])

        instance.name = validated_data.get('name', instance.name)
        instance.date_from = validated_data.get('date_from', instance.date_from)
        instance.date_to = validated_data.get('date_to', instance.date_to)
        instance.place = validated_data.get('place', instance.place)
        instance.place_region = validated_data.get('place_region', instance.place_region)
        instance.photos = validated_data.get('photos', instance.photos)
        instance.description = validated_data.get('description', instance.description)
        instance.registration_link = validated_data.get('registration_link', instance.registration_link)
        instance.hide_participants = validated_data.get('hide_participants', instance.hide_participants)
        instance.schedule_pdf = validated_data.get('schedule_pdf', instance.schedule_pdf)
        instance.extended_description = validated_data.get('extended_description', instance.extended_description)
        instance.co_organizer = validated_data.get('co_organizer', instance.co_organizer)
        instance.save()

        # Update or add competition types
        competition_types = []
        for comp in competition_type_data:
            competition_type_obj = None
            if 'id' in comp:
                competition_type_obj = CompetitionType.objects.filter(id=comp['id']).first()
            elif 'name' in comp:
                competition_type_obj = CompetitionType.objects.filter(name=comp['name']).first()

            if competition_type_obj:
                competition_types.append(competition_type_obj)
            else:
                raise serializers.ValidationError(
                    {'competition_type': f"Competition type '{comp.get('name', comp.get('id'))}' does not exist."})

        instance.competition_type.set(competition_types)

        # Handle distances (create, update, or delete)
        if distances_data is not None:
            existing_ids = [dist.id for dist in instance.distances.all()]
            input_ids = [item.get('id') for item in distances_data if 'id' in item]

            # Delete distances not in the input
            for dist_id in set(existing_ids) - set(input_ids):
                DistanceEvent.objects.filter(id=dist_id).delete()

            for distance_data in distances_data:
                distance_id = distance_data.get('id', None)
                if distance_id:
                    try:
                        distance_instance = DistanceEvent.objects.get(id=distance_id, event=instance)
                        # Use the DistanceEventSerializer to update the existing distance event
                        DistanceEventSerializer().update(distance_instance, distance_data)
                    except DistanceEvent.DoesNotExist:
                        # If distance event does not exist, create a new one
                        distance_data['event'] = instance
                        DistanceEventSerializer().create(distance_data)
                else:
                    # If no id, create a new distance event
                    distance_data['event'] = instance
                    DistanceEventSerializer().create(distance_data)

        return instance

    def get_organizer(self, obj):  # noqa
        organizer = Organizer.objects.filter(organization=obj.organization).first()
        return OrganizerSerializer(organizer).data if organizer else None


class UpdateEventStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=STATUS_CHOICES,
        required=True,
    )
