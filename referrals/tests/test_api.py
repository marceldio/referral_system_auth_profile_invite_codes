import pytest
from django.urls import reverse
from referrals.models import CustomUser


@pytest.mark.django_db
def test_send_code(api_client):
    # Используем корректное имя маршрута
    url = reverse('send-auth-code')
    response = api_client.post(url, {"phone_number": "+79167774613"})
    assert response.status_code == 200
    assert "message" in response.data


@pytest.mark.django_db
def test_verify_code(api_client, test_user):
    from django.core.cache import cache
    cache.set(f"auth_code_{test_user.phone_number}", 1234, timeout=300)

    # Используем корректное имя маршрута
    url = reverse('verify-auth-code')
    response = api_client.post(url, {"phone_number": test_user.phone_number, "auth_code": "1234"})
    assert response.status_code == 200
    assert response.data["message"] == "User verified successfully"


@pytest.mark.django_db
def test_activate_invite(api_client, test_user):
    api_client.force_authenticate(user=test_user)

    # Используем корректное имя маршрута
    url = reverse('activate-invite')
    inviter = CustomUser.objects.create_user(phone_number="+79168884422", invite_code="XYZ789")
    response = api_client.post(url, {"invite_code": inviter.invite_code})
    assert response.status_code == 200
    assert response.data["message"] == "Invite code activated successfully"
    assert test_user.profile.activated_invite_code == inviter.invite_code
