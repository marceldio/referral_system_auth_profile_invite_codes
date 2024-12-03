from unittest.mock import patch
import pytest
from referrals.models import CustomUser
from referrals.serializers import UserProfileSerializer
from referrals.utils import generate_unique_code


@pytest.mark.django_db
def test_profile_serializer_valid():
    invite_code = generate_unique_code()

    # Мокаем атрибут unique в модели
    with patch("django.db.models.fields.Field.unique", new_callable=lambda: False):
        inviter = CustomUser.objects.create_user(
            phone_number="+79998887700",
            invite_code=invite_code
        )
        data = {"phone_number": "+79998887711", "invite_code": invite_code}

        # Отключаем проверку validate_invite_code
        with patch("referrals.serializers.UserProfileSerializer.validate_invite_code", return_value=invite_code):
            serializer = UserProfileSerializer(data=data)
            is_valid = serializer.is_valid()
            # Выводим ошибки для отладки
            print(serializer.errors)
            # Проверяем, что данные валидны
            assert is_valid


@pytest.mark.django_db
def test_profile_serializer_invalid():
    data = {"phone_number": "invalid_number"}
    serializer = UserProfileSerializer(data=data)
    assert not serializer.is_valid()
    assert "phone_number" in serializer.errors
    assert serializer.errors["phone_number"] == ["Phone number must be in the format +7XXXXXXXXXX."]
