import os
import django
from django.core.cache import cache

# Укажите путь к файлу настроек вашего проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "referral_system.settings")

django.setup()

# Сохраняем данные в кэш
cache.set("test_key", "test_value", timeout=360)
print(f"Cached value: {cache.get('test_key')}")
