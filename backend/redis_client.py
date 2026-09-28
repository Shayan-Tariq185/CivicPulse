import redis

from config import settings

# Create a global Redis connection pool
redis_db = redis.Redis.from_url(
    settings.REDIS_URL,
    decode_responses=True # Automatically decodes byte strings to normal strings
)

def check_redis_health():
    """Simple ping to ensure Redis is alive."""
    try:
        return redis_db.ping()
    except redis.ConnectionError:
        return False
