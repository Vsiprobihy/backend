from rest_framework import serializers

from .models import PromoCode


class PromoCodeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = PromoCode
        fields = ['id', 'name', 'promo_type', 'discount_value', 'is_active', 'is_single_use', 'distance']
        extra_kwargs = {
            'distance': {'read_only': True}
        }
