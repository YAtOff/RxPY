from typing import Callable, TypeVar

import rx
from rx.core import Observable

_T = TypeVar("_T")


def _concat(*sources: Observable[_T]) -> Callable[[Observable[_T]], Observable[_T]]:
    def concat(source: Observable[_T]) -> Observable[_T]:
        """Concatenates all the observable sequences.

        Examples:
            >>> op = concat(xs, ys, zs)

        Returns:
            An operator function that takes one or more observable sources and
            returns an observable sequence that contains the elements of
            each given sequence, in sequential order.
        """
        return rx.concat(source, *sources)

    return concat


__all__ = ["_concat"]
