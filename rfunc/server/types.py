from concurrent.futures import Future
from typing import Callable, Protocol


class Pooler(Protocol):
    def schedule(
        self,
        function: Callable,
        args: tuple = (),
        kwargs: dict = {},
        timeout: float = 0,
    ) -> Future:
        ...
