from rest_framework import serializers

from event.models import AdditionalItemEvent
from event.models import Event


class AdditionalItemEventSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), required=False
    )

    class Meta:
        model = AdditionalItemEvent
        fields = ["id", "item_type", "price", "event"]
        extra_kwargs = {"event": {"read_only": True}}
