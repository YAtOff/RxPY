
import unittest

from nose import SkipTest
import sys
if sys.version_info.major < 3:
    raise SkipTest("Py3 language async language support required")

import rx
asyncio = rx.config['asyncio']
if asyncio is None:
    raise SkipTest("asyncio not available")
from rx.core import Observable, Disposable
from rx.testing import TestScheduler, ReactiveTest
from rx.disposables import SerialDisposable

on_next = ReactiveTest.on_next
on_completed = ReactiveTest.on_completed
on_error = ReactiveTest.on_error
subscribe = ReactiveTest.subscribe
subscribed = ReactiveTest.subscribed
disposed = ReactiveTest.disposed
created = ReactiveTest.created


class TestToFuture(unittest.TestCase):
    def test_await_success(self):
        result = None

        async def go():
            nonlocal result
            source = Observable.return_value(42)
            result = await source

        asyncio.run(go())
        assert(result == 42)
    def test_await_error(self):
        error = Exception("error")
        result = None

        async def go():
            nonlocal result
            source = Observable.throw(error)
            try:
                result = await source
            except Exception as ex:
                result = ex

        asyncio.run(go())
        assert(result == error)
