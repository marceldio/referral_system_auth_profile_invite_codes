import os
import django

# Укажите правильное имя модуля настроек
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'referral_system.settings')

# Инициализация Django
django.setup()

from django.core.cache import cache

# Тест работы с кэшем
cache.set('test_key', 'test_value', timeout=60)
print(f"Cached value: {cache.get('test_key')}")
