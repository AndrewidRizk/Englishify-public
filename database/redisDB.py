import redis
from redis.exceptions import ConnectionError, RedisError

def test_redis_connection():
    host = ""
    port = 
    password = ''
    try:
        r = redis.Redis(host=host, port=port, password=password, decode_responses=True)
        # Ping the Redis server
        if r.ping():
            print("Redis connection successful")
        else:
            print("Redis connection failed")
    except ConnectionError as e:
        print(f"Redis connection failed: {e}")
    except RedisError as e:
        print(f"Redis connection error: {e}")

# Replace with your Redis details
test_redis_connection()  # Omit password if not needed
