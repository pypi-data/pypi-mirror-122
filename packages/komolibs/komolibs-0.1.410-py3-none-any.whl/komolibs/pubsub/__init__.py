from aioredis import create_redis


async def check_redis_connection(url: str,
                                 port: int,
                                 password: str,
                                 db: int = 0,
                                 ssl: bool = True):
    val_in: str = 'value'
    val_out: any = None
    try:
        # Redis client bound to single connection (no auto reconnection).
        redis = await create_redis((url, port), db=db, password=password, ssl=ssl)

        await redis.set('test-connection-key', val_in)
        val_out = await redis.get('test-connection-key')

        # gracefully closing underlying connection
        redis.close()
        await redis.wait_closed()

    except Exception as e:
        pass

    if val_out.decode("utf-8") == val_in:
        return True
    else:
        raise Exception("Redis connection test failed. Check redis server status. ")
