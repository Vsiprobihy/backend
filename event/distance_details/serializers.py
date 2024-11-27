from rest_framework import serializers

from event.additional_items.models import AdditionalItemEvent
from event.additional_items.serializers import AdditionalItemEventSerializer
from event.distance_details.models import CostChangeRule, DistanceEvent
from event.models import Event


class CostChangeRuleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = CostChangeRule
        fields = ['id', 'cost', 'from_participants', 'from_date']


class DistanceEventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)
    additional_options = AdditionalItemEventSerializer(many=True, required=False)
    cost_change_rules = CostChangeRuleSerializer(many=True, required=False)  # New field

    class Meta:
        model = DistanceEvent
        fields = [
            'id', 'name', 'competition_type', 'category', 'allow_registration',
            'length', 'start_number_from', 'start_number_to', 'age_from', 'age_to',
            'cost', 'is_free', 'promo_only_registration',
            'show_name_on_number', 'show_start_number', 'event',
            'additional_options', 'cost_change_rules'
        ]
        extra_kwargs = {'event': {'read_only': True}}

    def create(self, validated_data):
        cost_change_rules_data = validated_data.pop('cost_change_rules', [])
        additional_options_data = validated_data.pop('additional_options', [])

        distance = DistanceEvent.objects.create(**validated_data)

        for option_data in additional_options_data:
            option_data['distance'] = distance
            AdditionalItemEvent.objects.create(**option_data)

        for rule_data in cost_change_rules_data:
            rule_data['distance'] = distance
            CostChangeRule.objects.create(**rule_data)

        return distance

    def update(self, instance, validated_data):
        cost_change_rules_data = validated_data.pop('cost_change_rules', None)
        additional_options_data = validated_data.pop('additional_options', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update cost change rules
        if cost_change_rules_data is not None:
            existing_ids = [rule.id for rule in instance.cost_change_rules.all()]
            input_ids = [item.get('id') for item in cost_change_rules_data if 'id' in item]

            # Delete rules not present in input
            for rule_id in set(existing_ids) - set(input_ids):
                CostChangeRule.objects.filter(id=rule_id).delete()

            # Update or create rules
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

        return instance

class PublicDistanceEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceEvent
        fields = ['name']
