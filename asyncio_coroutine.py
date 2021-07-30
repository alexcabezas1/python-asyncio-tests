import asyncio


async def coroutine():
    print("in coroutine")


loop = asyncio.get_event_loop()
try:
    print("starting coroutine")
    coro = coroutine()
    print("entering event loop")
    loop.run_until_complete(coro)
finally:
    print("closing event loop")
    loop.close()
