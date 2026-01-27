import asyncio
from app.infrastructures.redis.redisClient import RedisClient

async def main():
    rd = await RedisClient.instance()
    await rd.add("test_key", "hello")
    print(await rd.get("test_key"))

if __name__ == "__main__":
    asyncio.run(main())
