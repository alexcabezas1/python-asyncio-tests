import asyncio
import time
from threading import Thread


def mark_done(future, result):
    print('setting future result to {!r}'.format(result))
    time.sleep(1)
    future.set_result(result)


def another_work(n):
    print('another work {!r}'.format(n))


async def coro_func():
    return await asyncio.sleep(1, 42)


def start_worker(loop):
    asyncio.set_event_loop(loop)
    try:
        print("starting a second event loop")
        loop.run_forever()
    except KeyBoardInterrupt:
        print("closing the second event loop")
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        loop.stop()
        loop.close()


event_loop = asyncio.get_event_loop()

worker_loop = asyncio.new_event_loop()
worker = Thread(target=start_worker, args=(worker_loop,))
worker.start()

try:
    all_done = asyncio.Future()
    
    print('scheduling mark_done')
    event_loop.call_soon(mark_done, all_done, 'the result')
    event_loop.call_soon(another_work, 1000)

    worker_loop.call_soon_threadsafe(worker_loop.call_later, 1, another_work, 3000)
    worker_loop.call_soon_threadsafe(another_work, 2000)
    future = asyncio.run_coroutine_threadsafe(coro_func(), worker_loop)
    print(future.result(4))

    print('entering event loop')
    result = event_loop.run_until_complete(all_done)
    print('returned result: {!r}'.format(result))
finally:
    print('closing event loop')
    event_loop.close()