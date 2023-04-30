import asyncio
import inspect
import logging
from concurrent.futures import Future
from typing import Any

import cloudpickle as pickle
import pip

logger = logging.getLogger("rfunc")


def install_requirements(requirements: tuple[str]):
    pip_args = []

    pip_args.append("install")

    for requirement in requirements:
        pip_args.append(requirement)

    pip.main(pip_args)


def on_handle(payload: bytes, requirements: tuple[str]) -> Any:
    f, args, kwargs = pickle.loads(payload)

    if len(requirements) > 0:
        install_requirements(requirements)

    if inspect.iscoroutinefunction(f):
        return asyncio.run(f(*args, **kwargs))

    return f(*args, **kwargs)


def on_done(future: Future, *, transport: asyncio.Transport):
    peername = transport.get_extra_info("peername")

    try:
        result = future.result() or future.exception()
        transport.write(pickle.dumps(result))
    finally:
        transport.write_eof()
        logger.info("%s connection closed", peername)
