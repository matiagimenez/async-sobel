import redis
import os


def redis_connect():
    redis_port = os.environ.get('REDIS_PORT')
    redis_host = os.environ.get('REDIS_HOST')
    print(redis_host)
    print(redis_port)
    # redis_port = int(redis_port)

    return redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
