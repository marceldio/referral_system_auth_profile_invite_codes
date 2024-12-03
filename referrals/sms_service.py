import base64
import os
import requests
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()


def send_sms(phone_number, message):
    """
    Функция для отправки SMS через SMS Aero API.
    """
    url = "https://gate.smsaero.ru/v2/sms/send"
    payload = {
        # Номер телефона
        'number': phone_number,

        # Сообщение
        'text': message,

        # Подпись (не более 11 символов, для тестов использовать 'SMS Aero'в .env)
        'sign': os.getenv('SMS_AERO_SIGN'),

        # Канал отправки
        'channel': 'INFO',

        # Режим тестирования включен, для отключения закомментируйте эту строку
        'test': os.getenv('TEST_MODE', '1')
    }

    # Формируем заголовок Authorization с Base64-кодированием email и API-ключа
    email = os.getenv('SMSAERO_EMAIL')
    api_key = os.getenv('SMSAERO_API_KEY')
    if not email or not api_key:
        raise ValueError("Проверьте переменные окружения: SMS_AERO_EMAIL и SMS_AERO_API_KEY")

    credentials = f"{email}:{api_key}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/json'
    }

    # Отправляем запрос на сервер
    response = requests.post(url, json=payload, headers=headers)
    return response


if __name__ == "__main__":
    """
    Тестовый вызов функции для отправки SMS.
    """
    # Номер телефона из .env или по умолчанию
    phone_number = os.getenv('PHONE_NUMBER', '+79167774613')
    # Сообщение из .env или по умолчанию
    text_message = os.getenv('TEXT_MESSAGE', 'Это тестовое сообщение.')

    response = send_sms(phone_number, text_message)

    # Выводим результат:
    # HTTP статус-код
    print(response.status_code)
    # Тело ответа
    print(response.json())
