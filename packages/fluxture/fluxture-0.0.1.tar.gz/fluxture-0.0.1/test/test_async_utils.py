import asyncio
from time import sleep
from typing import List, Tuple
from unittest import TestCase

from fluxture.async_utils import iterator_to_async, sync_to_async


@iterator_to_async(poll_interval=0.24)
def slow_iterator(n: int):
    for i in range(n):
        sleep(0.5)
        yield i


async def slow_iterator_async(n: int) -> List[Tuple[int, float]]:
    loop = asyncio.get_running_loop()
    results = []
    async for i in slow_iterator(n):
        results.append((i, loop.time()))
    return results


async def sleep_and_return_time(duration: float) -> float:
    loop = asyncio.get_running_loop()
    await asyncio.sleep(duration)
    return loop.time()


async def slow_iterator_test(test: TestCase, n: int):
    slow_iterator_results, sleep_time = await asyncio.gather(slow_iterator_async(n), sleep_and_return_time(n / 2.0))
    expected = 0
    has_time_before = False
    has_time_after = False
    for i, end_time in slow_iterator_results:
        test.assertEqual(i, expected)
        expected += 1
        has_time_before = has_time_before or end_time < sleep_time
        has_time_after = has_time_after or end_time > sleep_time
    # ensure that asyncio actually scheduled `sleep_and_return` interleaved between `slow_iterator_async` iterations:
    test.assertTrue(has_time_before)
    test.assertTrue(has_time_after)


@sync_to_async(poll_interval=0.25)
def slow_function():
    sleep(2.0)


async def time_slow_function() -> float:
    loop = asyncio.get_running_loop()
    await slow_function()
    return loop.time()


async def slow_function_test(test: TestCase):
    slow_func_end_time, sleep_time = await asyncio.gather(time_slow_function(), sleep_and_return_time(1.0))
    # ensure that asyncio actually scheduled `sleep_and_return` before `time_slow_function`:
    test.assertLessEqual(sleep_time, slow_func_end_time)


class TestAsyncUtils(TestCase):
    def test_iterator_to_async(self):
        asyncio.run(slow_iterator_test(self, 10))

    def test_sync_to_async(self):
        asyncio.run(slow_function_test(self))
