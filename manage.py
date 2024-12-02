#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""

import sys
import os
from dotenv import load_dotenv

# Определяем BASE_DIR относительно settings.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Загружаем .env файл из корня проекта
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(env_path)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "referral_system.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
