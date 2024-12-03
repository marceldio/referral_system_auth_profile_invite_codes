from unittest.mock import patch
import pytest
from referrals.models import CustomUser
from referrals.serializers import UserProfileSerializer
from referrals.utils import generate_unique_code


@pytest.mark.django_db
def test_profile_serializer_invalid():
    data = {"phone_number": "invalid_number"}
    serializer = UserProfileSerializer(data=data)
    assert not serializer.is_valid()
    assert "phone_number" in serializer.errors
    assert serializer.errors["phone_number"] == ["Phone number must be in the format +7XXXXXXXXXX."]
