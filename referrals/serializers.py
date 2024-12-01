from rest_framework import serializers
from .models import CustomUser, Profile


class UserProfileSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'invite_code', 'profile', 'referrals']

    def get_profile(self, obj):
        if hasattr(obj, 'profile'):
            return {
                'activated_invite_code': obj.profile.activated_invite_code
            }
        return None

    def get_referrals(self, obj):
        from .models import Referral
        referrals = Referral.objects.filter(inviter=obj)
        return [{'invited_user_id': r.invited.id, 'invited_phone_number': r.invited.phone_number} for r in referrals]
