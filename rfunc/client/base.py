import abc
from typing import Any, Callable

import cloudpickle as pickle
import msgpack

from .errors import RemoteException
from .types import Response


class RFuncBaseClient(abc.ABC):
    def decode(self, data: bytes) -> Any:
        """
        Decodes bytes to python object.
        """
        result = pickle.loads(data)
        if isinstance(result, BaseException):
            raise RemoteException(result) from result
        return result

    def encode(self, f: Callable, args: tuple = (), kwargs: dict = {}) -> bytes:
        """
        Encodes python function object to bytes.
        """
        return pickle.dumps((f, args, kwargs))

    def prepare_data(
        self,
        f: Callable,
        args: tuple = (),
        kwargs: dict = {},
        timeout: float = 0,
        requirements: tuple[str, ...] = (),
    ) -> bytes:
        response: Response = {
            "payload": self.encode(f, args, kwargs),
            "requirements": requirements,
            "timeout": timeout,
        }
        return msgpack.packb(response)  # type: ignore

    @abc.abstractmethod
    async def send_data_async(self, data: bytes) -> bytes:
        ...

    @abc.abstractmethod
    def send_data_sync(self, data: bytes) -> bytes:
        ...
