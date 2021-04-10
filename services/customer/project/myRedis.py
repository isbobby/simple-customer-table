import redis
"""
note - In docker compose, the redis container is named 'redis', when debugging on localhost, the
redis server will run on localhost instead, so the host name has to be changed to 'localhost'
"""

"""
This redis cache stores the session IDs as an implementation to defend against stolen tokens
"""
redis_session_list = redis.StrictRedis(
    host="redis", port=6379, db=0, decode_responses=True
)

"""
This redis cache stores the expired tokens so that they can't be reused
"""
jwt_redis_block_list = redis.StrictRedis(
    host="redis", port=6379, db=0, decode_responses=True
)
