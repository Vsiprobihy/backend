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
    additional_options = AdditionalItemEventSerializer(many=True, required=False)
    cost_change_rules = CostChangeRuleSerializer(many=True, required=False)
    age_categories = AgeCategorySerializer(many=True, required=False)
    promo_codes = PromoCodeSerializer(many=True, required=False)

    class Meta:
        model = DistanceEvent
        fields = [
            'id', 'name', 'competitionType', 'category', 'allow_registration',
            'length', 'start_number_from', 'start_number_to', 'ageFrom', 'ageTo',
            'cost', 'is_free', 'promo_only_registration',
            'show_name_on_number', 'show_start_number', 'event',
            'additional_options', 'cost_change_rules', 'age_categories', 'promo_codes'
        ]
        extra_kwargs = {'event': {'read_only': True}}

    def create(self, validated_data):
        cost_change_rules_data = validated_data.pop('cost_change_rules', [])
        additional_options_data = validated_data.pop('additional_options', [])
        age_categories_data = validated_data.pop('age_categories', [])
        promo_codes_data = validated_data.pop('promo_codes', [])

        distance = DistanceEvent.objects.create(**validated_data)

        for option_data in additional_options_data:
            option_data['distance'] = distance
            AdditionalItemEvent.objects.create(**option_data)

        for rule_data in cost_change_rules_data:
            rule_data['distance'] = distance
            CostChangeRule.objects.create(**rule_data)

        for age_category_data in age_categories_data:
            age_category_data['distance'] = distance
            AgeCategory.objects.create(**age_category_data)

        for promo_code_data in promo_codes_data:
            promo_code_data['distance'] = distance
            PromoCode.objects.create(**promo_code_data)

        return distance

    def update(self, instance, validated_data):
        cost_change_rules_data = validated_data.pop('cost_change_rules', None)
        additional_options_data = validated_data.pop('additional_options', None)
        age_categories_data = validated_data.pop('age_categories', None)
        promo_codes_data = validated_data.pop('promo_codes', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update cost change rules
        if cost_change_rules_data is not None:
            existing_ids = [rule.id for rule in instance.cost_change_rules.all()]
            input_ids = [item.get('id') for item in cost_change_rules_data if 'id' in item]

            for rule_id in set(existing_ids) - set(input_ids):
                CostChangeRule.objects.filter(id=rule_id).delete()

            for rule_data in cost_change_rules_data:
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
        if additional_options_data is not None:
            existing_ids = [opt.id for opt in instance.additional_options.all()]
            input_ids = [item.get('id') for item in additional_options_data if 'id' in item]

            for opt_id in set(existing_ids) - set(input_ids):
                AdditionalItemEvent.objects.filter(id=opt_id).delete()

            for option_data in additional_options_data:
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
        if age_categories_data is not None:
            existing_ids = [cat.id for cat in instance.age_categories.all()]
            input_ids = [item.get('id') for item in age_categories_data if 'id' in item]

            for cat_id in set(existing_ids) - set(input_ids):
                AgeCategory.objects.filter(id=cat_id).delete()

            for age_category_data in age_categories_data:
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
        if promo_codes_data is not None:
            existing_ids = [promo.id for promo in instance.promo_codes.all()]
            input_ids = [item.get('id') for item in promo_codes_data if 'id' in item]

            for promo_id in set(existing_ids) - set(input_ids):
                PromoCode.objects.filter(id=promo_id).delete()

            for promo_code_data in promo_codes_data:
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
