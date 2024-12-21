from rest_framework import serializers

from event.additional_items.models import AdditionalItemEvent
from event.additional_items.serializers import AdditionalItemEventSerializer
from event.age_category.models import AgeCategory
from event.age_category.serializers import AgeCategorySerializer
from event.distance_details.models import CostChangeRule, DistanceEvent, FavoriteDistance
from event.models import Event
from event.promo_code.models import PromoCode
from event.promo_code.serializers import PromoCodeSerializer


class CostChangeRuleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = CostChangeRule
        fields = ['id', 'cost', 'fromParticipants', 'fromDate']


class DistanceEventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
    additionalOptions = AdditionalItemEventSerializer(many=True, required=False)
    costChangeRules = CostChangeRuleSerializer(many=True, required=False)
    ageCategories = AgeCategorySerializer(many=True, required=False)
    promoCodes = PromoCodeSerializer(many=True, required=False)

    class Meta:
        model = DistanceEvent
        fields = [
            'id', 'name', 'competitionType', 'category', 'allowRegistration',
            'length', 'startNumberFrom', 'startNumberTo', 'ageFrom', 'ageTo',
            'cost', 'isFree', 'promoOnlyRegistration',
            'showNameOnNumber', 'showStartNumber', 'event',
            'additionalOptions', 'costChangeRules', 'ageCategories', 'promoCodes'
        ]
        extra_kwargs = {'event': {'read_only': True}}

    def create(self, validated_data):
        costChangeRulesData = validated_data.pop('costChangeRules', [])
        additionalOptionsData = validated_data.pop('additionalOptions', [])
        ageCategoriesData = validated_data.pop('ageCategories', [])
        promoCodesData = validated_data.pop('promoCodes', [])

        distance = DistanceEvent.objects.create(**validated_data)

        for option_data in additionalOptionsData:
            option_data['distance'] = distance
            AdditionalItemEvent.objects.create(**option_data)

        for rule_data in costChangeRulesData:
            rule_data['distance'] = distance
            CostChangeRule.objects.create(**rule_data)

        for age_category_data in ageCategoriesData:
            age_category_data['distance'] = distance
            AgeCategory.objects.create(**age_category_data)

        for promo_code_data in promoCodesData:
            promo_code_data['distance'] = distance
            PromoCode.objects.create(**promo_code_data)

        return distance

    def update(self, instance, validated_data):
        costChangeRulesData = validated_data.pop('costChangeRules', None)
        additionalOptionsData = validated_data.pop('additionalOptions', None)
        ageCategoriesData = validated_data.pop('ageCategories', None)
        promoCodesData = validated_data.pop('promoCodes', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update cost change rules
        if costChangeRulesData is not None:
            existing_ids = [rule.id for rule in instance.costChangeRules.all()]
            input_ids = [item.get('id') for item in costChangeRulesData if 'id' in item]

            for rule_id in set(existing_ids) - set(input_ids):
                CostChangeRule.objects.filter(id=rule_id).delete()

            for rule_data in costChangeRulesData:
                rule_id = rule_data.get('id', None)
                if rule_id:
                    try:
                        rule_instance = CostChangeRule.objects.get(id=rule_id, distance=instance)
                        for attr, value in rule_data.items():
                            setattr(rule_instance, attr, value)
                        rule_instance.save()
                    except CostChangeRule.DoesNotExist:
                        rule_data['distance'] = instance
                        CostChangeRule.objects.create(**rule_data)
                else:
                    rule_data['distance'] = instance
                    CostChangeRule.objects.create(**rule_data)

        # Update additional options
        if additionalOptionsData is not None:
            existing_ids = [opt.id for opt in instance.additionalOptions.all()]
            input_ids = [item.get('id') for item in additionalOptionsData if 'id' in item]

            for opt_id in set(existing_ids) - set(input_ids):
                AdditionalItemEvent.objects.filter(id=opt_id).delete()

            for option_data in additionalOptionsData:
                option_id = option_data.get('id', None)
                if option_id:
                    try:
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

        # Update age categories
        if ageCategoriesData is not None:
            existing_ids = [cat.id for cat in instance.ageCategories.all()]
            input_ids = [item.get('id') for item in ageCategoriesData if 'id' in item]

            for cat_id in set(existing_ids) - set(input_ids):
                AgeCategory.objects.filter(id=cat_id).delete()

            for age_category_data in ageCategoriesData:
                cat_id = age_category_data.get('id', None)
                if cat_id:
                    try:
                        cat_instance = AgeCategory.objects.get(id=cat_id, distance=instance)
                        for attr, value in age_category_data.items():
                            setattr(cat_instance, attr, value)
                        cat_instance.save()
                    except AgeCategory.DoesNotExist:
                        age_category_data['distance'] = instance
                        AgeCategory.objects.create(**age_category_data)
                else:
                    age_category_data['distance'] = instance
                    AgeCategory.objects.create(**age_category_data)

        # Update promo codes
        if promoCodesData is not None:
            existing_ids = [promo.id for promo in instance.promoCodes.all()]
            input_ids = [item.get('id') for item in promoCodesData if 'id' in item]

            for promo_id in set(existing_ids) - set(input_ids):
                PromoCode.objects.filter(id=promo_id).delete()

            for promo_code_data in promoCodesData:
                promo_id = promo_code_data.get('id', None)
                if promo_id:
                    try:
                        promo_instance = PromoCode.objects.get(id=promo_id, distance=instance)
                        for attr, value in promo_code_data.items():
                            setattr(promo_instance, attr, value)
                        promo_instance.save()
                    except PromoCode.DoesNotExist:
                        promo_code_data['distance'] = instance
                        PromoCode.objects.create(**promo_code_data)
                else:
                    promo_code_data['distance'] = instance
                    PromoCode.objects.create(**promo_code_data)

        return instance


class FavoriteDistanceSerializer(serializers.ModelSerializer):
    distance = DistanceEventSerializer()

    class Meta:
        model = FavoriteDistance
        fields = ['id', 'user', 'distance']


class PublicDistanceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceEvent
        fields = ['name']
