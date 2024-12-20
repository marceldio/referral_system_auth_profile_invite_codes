# referral_system_auth_profile_invite_codes   - описание
"Реферальная система: мини-приложение с авторизацией, 
профилем и поддержкой инвайт-кодов"

Реализована реферальная система. Минимальный интерфейс для тестирования
Реализована логика и API для следующего функционала :

●	Авторизация по номеру телефона. 
   Первый запрос на ввод номера телефона. 

   Второй запрос на ввод кода 

●	Если пользователь ранее не авторизовывался, то записывается в бд 

●	Запрос на профиль пользователя

●	Пользователю при первой авторизации присваивается рандомно 
сгенерированный 6-значный инвайт-код(цифры и символы)

●	В профиле у пользователя есть возможность ввести чужой 
инвайт-код(при вводе производится проверка на существование). 
В своем профиле можно активировать только 1 инвайт код, если пользователь 
уже когда-то активировал инвайт код, то нужно выводить его в соответсвующем 
поле в запросе на профиль пользователя

●	В API профиля выводится список пользователей(номеров телефона), 
которые ввели инвайт код текущего пользователя.

# Referral System   - инструкция

Referral System — это веб-приложение для управления пользователями, 
их реферальными кодами и профилями.

## Основные функции
- Отправка и проверка кода авторизации по номеру телефона.
- Активация реферальных кодов.
- Управление профилями пользователей.
- Генерация токенов доступа для авторизации.

## Технологии
- **Python** 3.12
- **Django** 5.1
- **Django REST Framework**
- **PostgreSQL**
- **Redis**
- **Docker**

## Установка и запуск

### Локальная установка
1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/marceldio/referral_system_auth_profile_invite_codes.git
   cd referral_system

2. Установите зависимости (используется Poetry):
poetry install

3. Выполните миграции:
python manage.py migrate

4. Настройте файл .env:
Укажите данные для подключения к SMS-сервису smsaero.ru.
Если вы хотите отправлять реальные SMS, добавьте параметр:
ENABLE_SMS=True
Если ENABLE_SMS=False(как по-умолчанию), код авторизации будет отображаться:
В терминале.
В Redis:
redis-cli
SELECT 1
GET ":1:auth_code_+7ваш_номер_телефона"

5. Запустите сервер:
python manage.py runserver

6. Документация API:
Swagger: http://127.0.0.1:8000/swagger/
ReDoc: http://127.0.0.1:8000/redoc/

7. Тестирование
Запуск тестов:
poetry run pytest referrals/tests/
Проверка покрытия тестами:
poetry run pytest --cov=referrals referrals/tests/

8. Postman коллекция с запросами находится в корне проекта.
ReferralSystemAuthAPI.postman_collection.json

9. ## Установка и запуск с использованием Docker
Проект поддерживает использование Docker для упрощённой настройки и запуска. Следуйте этим шагам:

### Предварительные требования
- Установите [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/).
- Убедитесь, что порты 8000 (Django), 5432 (PostgreSQL), и 6379 (Redis) свободны на вашем устройстве.

### Шаги по запуску проекта с Docker

1. **Клонируйте репозиторий:**

2. **Проверьте и настройте файл `.env`:**
   Убедитесь, что переменные окружения правильно настроены в `.env`. 
Пример содержимого файла: sample.env


3. **Соберите и запустите контейнеры:**
   ```bash
   docker-compose up --build
   ```
   Контейнеры `app` (Django), `db` (PostgreSQL), и `redis` (Redis) будут автоматически запущены.

4. **Проверьте работоспособность:**
   - Swagger документация доступна по адресу: http://127.0.0.1:8000/swagger/
   - Redoc документация доступна по адресу: http://127.0.0.1:8000/redoc/

5. **Остановите контейнеры:**
   Чтобы остановить контейнеры, выполните:
   ```bash
   docker-compose down
   ```

### Часто возникающие проблемы

- **Порт 5432 (PostgreSQL) занят:**
  - Либо остановите локальный экземпляр PostgreSQL:
    ```bash
    sudo service postgresql stop
    ```
  - Либо измените внешний порт в `docker-compose.yml`:
    ```yaml
    ports:
      - "5433:5432"
    ```

- **Ошибка подключения к Redis:**
  Проверьте настройки `REDIS_HOST`, `REDIS_PORT` и `REDIS_PASSWORD` в `.env`.

- **Документация не доступна:**
  Убедитесь, что контейнеры запущены и сервер Django работает.
