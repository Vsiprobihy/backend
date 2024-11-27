from rest_framework import serializers

from .models import AgeCategory


class AgeCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = AgeCategory
        fields = ['id', 'name', 'gender', 'age_from', 'age_to', 'distance']
        extra_kwargs = {
            'distance': {'read_only': True}
        }
