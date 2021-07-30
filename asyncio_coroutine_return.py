import asyncio


async def coroutine():
    print("in coroutine")
    return "result"


loop = asyncio.get_event_loop()
try:
    return_value = loop.run_until_complete(coroutine())
    print("it returned: {!r}".format(return_value))
finally:
    loop.close()
    