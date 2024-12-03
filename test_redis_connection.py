import redis
import os
from dotenv import load_dotenv

# Загружаем переменные из.env
load_dotenv()


def test_redis_connection():
    redis_host = os.getenv('REDIS_HOST')
    redis_port = os.getenv('REDIS_PORT')
    redis_password = os.getenv('REDIS_PASSWORD')
    redis_db = os.getenv('REDIS_DB', 0)

    try:
        client = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            db=int(redis_db),
            decode_responses=True
        )
        client.ping()
        print("✅ Successfully connected to Redis!")
    except redis.ConnectionError as e:
        print("❌ Failed to connect to Redis:", str(e))

if __name__ == "__main__":
    test_redis_connection()
