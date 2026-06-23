from redis.asyncio import Redis 


redis_client : Redis | None = None 


async def init_redis() -> Redis:
    global redis_client

    redis_client = Redis.from_url(
        "redis://localhost:6379/0", 
        decode_responses = True , 
        socket_connect_timeout = 2 , 
        socket_timeout = 2
    )

    await redis_client.ping()
    return redis_client 

async def close_redis():
    global redis_client 

    if redis_client is not None:
        await redis_client.aclose()
        redis_client = None 


def get_redis():
    if not redis_client:
        raise RuntimeError("redis client not found")
    
    return redis_client