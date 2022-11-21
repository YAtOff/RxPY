import unittest

from nose import SkipTest
import rx
asyncio = rx.config['asyncio']
if asyncio is None:
    raise SkipTest("asyncio not available")
Future = rx.config['Future']

from rx import Observable
from asyncio import Future

class TestFromFuture(unittest.IsolatedAsyncioTestCase):

    async def test_future_success(self):
        completed = asyncio.Event()
        success = [False, True, False]

        async def go():
            future = Future()
            future.set_result(42)

            source = Observable.from_future(future)

            def on_next(x):
                success[0] = 42 == x

            def on_error(err):
                success[1] = False
                completed.set()

            def on_completed():
                success[2] = True
                completed.set()


            subscription = source.subscribe(on_next, on_error, on_completed)

        await go()
        await completed.wait()
        assert(all(success))

    async def test_future_failure(self):
        completed = asyncio.Event()
        success = [True, False, True]

        async def go():
            error = Exception('woops')

            future = Future()
            future.set_exception(error)

            source = Observable.from_future(future)

            def on_next(x):
                success[0] = False

            def on_error(err):
                success[1] = str(err) == str(error)
                completed.set()

            def on_completed():
                success[2] = False
                completed.set()

            subscription = source.subscribe(on_next, on_error, on_completed)

        await go()
        await completed.wait()
        assert(all(success))

    async def test_future_dispose(self):
        success = [True, True, True]

        async def go():
            future = Future()
            future.set_result(42)

            source = Observable.from_future(future)

            def on_next(x):
                success[0] = False

            def on_error(err):
                success[1] = False

            def on_completed():
                success[2] = False

            subscription = source.subscribe(on_next, on_error, on_completed)
            subscription.dispose()

        await go()
        assert(all(success))
