from rest_framework import serializers

from event.models import DistanceEvent, AdditionalItemEvent, EventRegistration


class EventRegistrationDetailSerializer(serializers.ModelSerializer):
    distances = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=DistanceEvent.objects.all()
    )
    additional_items = serializers.SlugRelatedField(
        many=True, slug_field="item_type", queryset=AdditionalItemEvent.objects.all()
    )

    class Meta:
        model = EventRegistration
        fields = [
            "event",
            "distances",
            "additional_items",
            "registration_date",
            "is_confirmed",
        ]


class EventRegistrationSerializer(serializers.ModelSerializer):
    distances = serializers.PrimaryKeyRelatedField(
        queryset=DistanceEvent.objects.all(), many=True
    )
    additional_items = serializers.PrimaryKeyRelatedField(
        queryset=AdditionalItemEvent.objects.all(), many=True
    )

    class Meta:
        model = EventRegistration
        fields = [
            "event",
            "distances",
            "additional_items",
            "registration_date",
            "is_confirmed",
        ]
        read_only_fields = ["registration_date", "is_confirmed"]

    def validate(self, data):
        if not data.get("distances"):
            raise serializers.ValidationError("At least one distance must be selected.")
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        event = validated_data["event"]
        additional_items_data = validated_data.pop("additional_items", [])
        distances_data = validated_data.pop("distances", [])

        print("Received additional_items:", additional_items_data)
        print("Received distances:", distances_data)

        registration = EventRegistration.objects.create(user=user, event=event)

        registration.distances.set(distances_data)

        if additional_items_data:
            print("Setting additional_items:", additional_items_data)
            registration.additional_items.set(additional_items_data)
        else:
            print("No additional items to set.")

        registration.save()
        return registration
