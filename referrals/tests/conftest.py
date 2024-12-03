import pytest
from rest_framework.test import APIClient
from referrals.models import CustomUser
from django.db import connection
from django.test import TestCase
from django.db import connections
from django.db.utils import OperationalError



@pytest.fixture(autouse=True)
def clear_db():
    """
    Очистка базы данных перед каждым тестом.
    """
    TestCase()._pre_setup()


@pytest.fixture(autouse=True)
def reset_sequences():
    for connection in connections.all():
        try:
            cursor = connection.cursor()
            cursor.execute("SET CONSTRAINTS ALL DEFERRED;")
            cursor.execute("TRUNCATE TABLE django_migrations RESTART IDENTITY CASCADE;")
        except OperationalError:
            pass


@pytest.fixture(scope="function", autouse=True)
def disable_unique_constraints():
    """
    Отключает ограничения уникальности в базе данных для тестов.
    """
    with connection.cursor() as cursor:
        cursor.execute("SET CONSTRAINTS ALL DEFERRED;")
        yield
        cursor.execute("SET CONSTRAINTS ALL IMMEDIATE;")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    return CustomUser.objects.create_user(phone_number="+79167774613", invite_code="ABC123")
