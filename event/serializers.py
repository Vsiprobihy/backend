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
    competitionType = CompetitionTypeSerializer(many=True)
    organizer = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'organizer', 'organization_id', 'competitionType', 'dateFrom', 'dateTo',
            'place', 'placeRegion',
            'photos', 'description', 'registrationLink', 'hideParticipants', 'schedulePdf',
            'coOrganizer', 'distances', 'extendedDescription',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is None:
            self.fields['distances'].required = True
        else:
            self.fields['distances'].required = False

        self.fields['name'].required = True
        self.fields['competitionType'].required = True
        self.fields['dateFrom'].required = True
        self.fields['dateTo'].required = True
        self.fields['place'].required = True
        self.fields['placeRegion'].required = True
        self.fields['description'].required = False
        self.fields['registrationLink'].required = False
        self.fields['hideParticipants'].required = False
        self.fields['schedulePdf'].required = False
        self.fields['extendedDescription'].required = False
        self.fields['coOrganizer'].required = False

    def validate(self, data):
        instanceDateFrom = getattr(self.instance, 'dateFrom', None)
        instanceDateTo = getattr(self.instance, 'dateTo', None)

        dateFrom = data.get('dateFrom', instanceDateFrom)
        dateTo = data.get('dateTo', instanceDateTo)

        if dateFrom and dateTo:
            if dateTo < dateFrom:
                raise serializers.ValidationError({
                    'dateTo': 'The end date cannot be earlier than the start date.',
                    'dateFrom': 'The start date cannot be later than the end date.'
                })

        return data

    def create(self, validated_data):
        organization_id = validated_data.pop('organization_id')
        distances_data = validated_data.pop('distances')
        competitionTypeData = validated_data.pop('competitionType', [])

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

        competitionTypes = []
        for comp in competitionTypeData:
            competitionType = CompetitionType.objects.get(name=comp['name'])
            competitionTypes.append(competitionType)

        event.competitionType.set(competitionTypes)

        for distance_data in distances_data:
            additionalOptionsData = distance_data.pop('additionalOptions', [])
            costChangeRulesData = distance_data.pop('costChangeRules', [])
            ageCategoriesData = distance_data.pop('ageCategories', [])
            promoCodesData = distance_data.pop('promoCodes', [])

            distance = DistanceEvent.objects.create(event=event, **distance_data)

            for option_data in additionalOptionsData:
                option_data['distance'] = distance
                AdditionalItemEvent.objects.create(**option_data)

            for rule_data in costChangeRulesData:
                rule_data['distance'] = distance
                CostChangeRule.objects.create(**rule_data)

            for category_data in ageCategoriesData:
                category_data['distance'] = distance
                AgeCategory.objects.create(**category_data)

            for promo_code_data in promoCodesData:
                promo_code_data['distance'] = distance
                PromoCode.objects.create(**promo_code_data)

        return event

    def update(self, instance, validated_data):
        distances_data = validated_data.pop('distances', None)
        competitionTypeData = validated_data.pop('competitionType', [])

        instance.name = validated_data.get('name', instance.name)
        instance.dateFrom = validated_data.get('dateFrom', instance.dateFrom)
        instance.dateTo = validated_data.get('dateTo', instance.dateTo)
        instance.place = validated_data.get('place', instance.place)
        instance.placeRegion = validated_data.get('placeRegion', instance.placeRegion)
        instance.photos = validated_data.get('photos', instance.photos)
        instance.description = validated_data.get('description', instance.description)
        instance.registrationLink = validated_data.get('registrationLink', instance.registrationLink)
        instance.hideParticipants = validated_data.get('hideParticipants', instance.hideParticipants)
        instance.schedulePdf = validated_data.get('schedulePdf', instance.schedulePdf)
        instance.extendedDescription = validated_data.get('extendedDescription', instance.extendedDescription)
        instance.coOrganizer = validated_data.get('coOrganizer', instance.coOrganizer)
        instance.save()

        # Update or add competition types
        competitionTypes = []
        for comp in competitionTypeData:
            competitionTypeObj = None
            if 'id' in comp:
                competitionTypeObj = CompetitionType.objects.filter(id=comp['id']).first()
            elif 'name' in comp:
                competitionTypeObj = CompetitionType.objects.filter(name=comp['name']).first()

            if competitionTypeObj:
                competitionTypes.append(competitionTypeObj)
            else:
                raise serializers.ValidationError(
                    {'competitionType': f"Competition type '{comp.get('name', comp.get('id'))}' does not exist."})

        instance.competitionType.set(competitionTypes)

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
