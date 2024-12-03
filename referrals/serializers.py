from rest_framework import serializers
from referrals.models import CustomUser
from django.core.validators import RegexValidator
from drf_spectacular.utils import extend_schema_field


class SendAuthCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        help_text="Введите номер телефона в формате +7XXXXXXXXXX."
    )


class VerifyAuthCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        help_text="Введите номер телефона в формате +7XXXXXXXXXX.",
        validators=[
            RegexValidator(
                regex=r'^\+7\d{10}$',
                message="Phone number must be in the format +7XXXXXXXXXX.",
                code='invalid_phone_number'
            )
        ]
    )
    auth_code = serializers.CharField(
        help_text="Введите код, отправленный на ваш номер телефона."
    )


class ActivateInviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(
        help_text="Введите инвайт-код, который вы хотите активировать."
    )


class UserProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+7\d{10}$',
                message="Phone number must be in the format +7XXXXXXXXXX.",
                code='invalid_phone_number'
            )
        ]
    )
    profile = serializers.SerializerMethodField()
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'invite_code', 'profile', 'referrals']

    @extend_schema_field({
        'type': 'object',
        'properties': {
            'activated_invite_code': {'type': 'string', 'nullable': True},
        }
    })
    def get_profile(self, obj):
        if hasattr(obj, 'profile') and obj.profile:
            return {
                'activated_invite_code': obj.profile.activated_invite_code
            }
        return None

    @extend_schema_field({
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'invited_user_id': {'type': 'integer'},
                'invited_phone_number': {'type': 'string'},
            }
        }
    })
    def get_referrals(self, obj):
        from .models import Referral
        referrals = Referral.objects.filter(inviter=obj)
        return [
            {
                'invited_user_id': r.invited.id,
                'invited_phone_number': r.invited.phone_number
            }
            for r in referrals
        ]
