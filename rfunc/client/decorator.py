import inspect
from typing import Any, Callable

from .base import RFuncBaseClient


class RFunc:
    def __init__(self, client: RFuncBaseClient) -> None:
        self.client = client

    def get_wrapper_func(
        self, f: Callable, timeout: float = 0, requirements: tuple[str, ...] = ()
    ) -> Callable:
        if inspect.iscoroutinefunction(f):

            async def wrapper_async(*args, **kwargs) -> Any:
                data = self.client.prepare_data(f, args, kwargs, timeout, requirements)
                response = await self.client.send_data_async(data)
                return self.client.decode(response)

            return wrapper_async
        else:

            def wrapper_sync(*args, **kwargs) -> Any:
                data = self.client.prepare_data(f, args, kwargs, timeout, requirements)
                response = self.client.send_data_sync(data)
                return self.client.decode(response)

            return wrapper_sync

    def __call__(
        self, timeout: float = 0, requirements: tuple[str, ...] = ()
    ) -> Callable:
        def decorator(f: Callable) -> Callable:
            return self.get_wrapper_func(f, timeout, requirements)

        return decorator
