import redis

"""
This redis cache stores the session IDs as an implementation to defend against stolen tokens
"""
redis_session_list = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

"""
This redis cache stores the expired tokens so that they can't be reused
"""
jwt_redis_block_list = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)
