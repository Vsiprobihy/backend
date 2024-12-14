from io import BytesIO

from django.contrib.auth import get_user_model
from PIL import Image
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from authentication.models import AdditionalProfile, CustomUser


def validate_password_confirm(password, password2):
    if password != password2:
        raise serializers.ValidationError('Passwords must match')
    return True


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'password2']

    @staticmethod
    def validate_password(value):
        """
        Ensure that the password contains at least:
        - 1 uppercase letter
        - 1 special character
        - 1 number
        """
        # if not re.search(r'[A-Z]', value):
        #     raise ValidationError('Password must contain at least 1 uppercase letter.')
        #
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        #     raise ValidationError('Password must contain at least 1 special character.')
        #
        # if not re.search(r'\d', value):
        #     raise ValidationError('Password must contain at least 1 number.')

        return value

    def validate(self, data):
        validate_password_confirm(data['password'], data['password2'])
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = get_user_model().objects.create_user(**validated_data)
        # user.is_active = False
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'first_name_eng',
            'last_name_eng',
            'gender',
            'date_of_birth',
            't_shirt_size',
            'country',
            'city',
            'phone_number',
            'sports_club',
            'emergency_contact_name',
            'emergency_contact_phone',
            'avatar',
            'email',
        ]

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_email(self, obj):
        return obj.email


class UserAvatarUploadSerializer(serializers.ModelSerializer):
    def validate_avatar(self, value):
        if value:
            if not value.name.endswith(('.png', '.jpg', '.jpeg')):
                raise ValidationError(
                    'Invalid file format. Only PNG, JPG, and JPEG are allowed.'
                )

            if value.size > 3 * 1024 * 1024:
                raise ValidationError('File size exceeds the 3 MB limit.')

            image = Image.open(value)

            # If the image is in RGBA, convert it to RGB (remove alpha channel)
            if image.mode == 'RGBA':
                image = image.convert('RGB')

            image.thumbnail((300, 300))

            thumb_io = BytesIO()
            image.save(thumb_io, format='JPEG')
            thumb_io.seek(0)

            value = thumb_io

        return value

    class Meta:
        model = CustomUser
        fields = ['avatar']


class AdditionalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalProfile
        fields = '__all__'


class AdditionalProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalProfile
        fields = '__all__'
