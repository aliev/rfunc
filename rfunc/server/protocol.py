import asyncio
import functools
import logging
from typing import TYPE_CHECKING

import cloudpickle as pickle
import msgpack
from pebble import ProcessPool

from ..client.types import Response
from .errors import MessageException
from .handlers import on_done, on_handle

logger = logging.getLogger("rfunc")


class RFuncProtocol(asyncio.Protocol):
    def __init__(self, pool: ProcessPool):
        self.pool = pool
        self.transport: asyncio.Transport | None = None
        self.peername: str | None = None

    def connection_made(self, transport: asyncio.Transport):  # type: ignore
        self.peername = transport.get_extra_info("peername")
        self.transport = transport
        logger.info("%s connected", self.peername)

    def data_received(self, data: bytes):
        if TYPE_CHECKING:
            assert self.transport is not None

        try:
            response: Response = msgpack.unpackb(data)
        except Exception:
            logger.error("%s cannot parse message", self.peername)
            self.transport.write(pickle.dumps(MessageException("Cannot parse message")))
            self.transport.write_eof()
            return

        on_done_ = functools.partial(on_done, transport=self.transport)

        future = self.pool.schedule(
            on_handle,
            [response["payload"], response["requirements"]],
            timeout=response["timeout"],
        )

        future.add_done_callback(on_done_)
