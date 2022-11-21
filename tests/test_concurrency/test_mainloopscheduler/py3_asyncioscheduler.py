from nose import SkipTest

import rx
asyncio = rx.config['asyncio']
if asyncio is None:
    raise SkipTest("asyncio not available")

import unittest

from datetime import datetime, timedelta
from rx.concurrency import AsyncIOScheduler


class TestAsyncIOScheduler(unittest.IsolatedAsyncioTestCase):
    async def test_asyncio_schedule_now(self):
        loop = asyncio.get_event_loop()
        scheduler = AsyncIOScheduler(loop)
        res = scheduler.now - datetime.now()
        assert(res < timedelta(seconds=1))

    async def test_asyncio_schedule_action(self):
        async def go():
            loop = asyncio.get_event_loop()
            scheduler = AsyncIOScheduler(loop)
            ran = False

            def action(scheduler, state):
                nonlocal ran
                ran = True
            scheduler.schedule(action)

            await asyncio.sleep(0.1)
            assert(ran is True)

        await go()

    async def test_asyncio_schedule_action_due(self):
        async def go():
            loop = asyncio.get_event_loop()
            scheduler = AsyncIOScheduler(loop)
            starttime = loop.time()
            endtime = None

            def action(scheduler, state):
                nonlocal endtime
                endtime = loop.time()

            scheduler.schedule_relative(200, action)

            await asyncio.sleep(0.3)
            diff = endtime-starttime
            assert(diff > 0.18)

        await go()

    async def test_asyncio_schedule_action_cancel(self):
        async def go():
            ran = False
            loop = asyncio.get_event_loop()
            scheduler = AsyncIOScheduler(loop)

            def action(scheduler, state):
                nonlocal ran
                ran = True
            d = scheduler.schedule_relative(10, action)
            d.dispose()

            await asyncio.sleep(0.1)
            assert(not ran)

        await go()
