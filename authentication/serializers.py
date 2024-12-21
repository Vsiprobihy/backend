from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from rest_framework import serializers

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
        fields = [
            'email',
            'password',
            'password2',
            'firstName',
            'lastName',
            'phoneNumber',
            'dateOfBirth',
            'gender',
            'dateOfBirth',
            'tShirtSize',
            'country',
            'city',
            'phoneNumber',
            'sportsClub',
            'emergencyContactName',
            'emergencyContactPhone',
        ]

    @staticmethod
    def validate_password(value):   #ToDO:  повернути на проді
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
        # user.isActive = False  #ToDO:  повернути на проді
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(default='user@example.com')
    password = serializers.CharField(default='string')


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'role',
            'firstName',
            'lastName',
            'firstNameEng',
            'lastNameEng',
            'gender',
            'dateOfBirth',
            'tShirtSize',
            'country',
            'city',
            'phoneNumber',
            'sportsClub',
            'emergencyContactName',
            'emergencyContactPhone',
            'avatar',
        ]

    def update(self, instance, validated_data):
        avatar = validated_data.pop('avatar', None)
        if avatar:
            if instance.avatar:
                try:
                    if default_storage.exists(instance.avatar.path):
                        default_storage.delete(instance.avatar.path)
                except ObjectDoesNotExist:
                    pass

            instance.avatar = avatar

        return super().update(instance, validated_data)

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_email(self, obj):  # noqa
        return obj.email


class AdditionalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalProfile
        fields = '__all__'


class AdditionalProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalProfile
        fields = '__all__'
