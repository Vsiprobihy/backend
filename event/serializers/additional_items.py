from rest_framework import serializers

from event.models import AdditionalItemEvent, DistanceEvent, OrganizationAccess


class AdditionalItemEventSerializer(serializers.ModelSerializer):
    distance = serializers.PrimaryKeyRelatedField(queryset=DistanceEvent.objects.all(), required=False)

    class Meta:
        model = AdditionalItemEvent
        fields = ['id', 'item_type', 'price', 'distance']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def validate(self, data):
        user = self.context['request'].user
        distance = data.get('distance', None)

        if distance and not OrganizationAccess.objects.filter(
            organization_id=distance.event.organizer.id,
            user=user
        ).exists():
            raise serializers.ValidationError({
                'distance': 'You do not have access to the organization associated with this distance.'
            })

        return data
