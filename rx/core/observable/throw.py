from typing import Any, Optional, Union

from rx.core import Observable, abc
from rx.scheduler import ImmediateScheduler


def _throw(
    exception: Union[str, Exception], scheduler: Optional[abc.SchedulerBase] = None
) -> Observable[Any]:
    exception = exception if isinstance(exception, Exception) else Exception(exception)

    def subscribe(
        observer: abc.ObserverBase[Any], scheduler: Optional[abc.SchedulerBase] = None
    ) -> abc.DisposableBase:
        _scheduler = scheduler or ImmediateScheduler.singleton()

        def action(scheduler: abc.SchedulerBase, state: Any):
            observer.on_error(exception)

        return _scheduler.schedule(action)

    return Observable(subscribe)


__all__ = ["_throw"]
