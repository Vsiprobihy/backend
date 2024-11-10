from rest_framework import serializers

from event.models import DistanceEvent, Event


class DistanceEventSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), required=False
    )

    class Meta:
        model = DistanceEvent
        fields = [
            "id",
            "name",
            "competition_type",
            "category",
            "allow_registration",
            "length",
            "start_number_from",
            "start_number_to",
            "age_from",
            "age_to",
            "cost",
            "is_free",
            "promo_only_registration",
            "show_name_on_number",
            "show_start_number",
            "event",
        ]
        extra_kwargs = {"event": {"read_only": True}}
