from rest_framework import serializers
from referrals.models import CustomUser
from django.core.validators import RegexValidator


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

    def get_profile(self, obj):
        if hasattr(obj, 'profile') and obj.profile:
            return {
                'activated_invite_code': obj.profile.activated_invite_code
            }
        return None

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
