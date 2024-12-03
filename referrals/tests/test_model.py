import pytest
from referrals.models import CustomUser

@pytest.mark.django_db
def test_create_user():
    user = CustomUser.objects.create_user(phone_number="+79998887766", password="testpass")
    assert user.phone_number == "+79998887766"
    assert user.check_password("testpass")

@pytest.mark.django_db
def test_invite_code():
    user = CustomUser.objects.create_user(phone_number="+79998887777", invite_code="XYZ123")
    assert user.invite_code == "XYZ123"
