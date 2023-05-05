import argparse
import asyncio
import logging

from pebble import ProcessPool

from .protocol import RFuncProtocol

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger("rfunc")


async def main(pool: ProcessPool, host: str, port: int):
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: RFuncProtocol(
            pool,
        ),
        host,
        port,
    )

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Runs python remote functions execution server."
    )
    parser.add_argument(
        "--host",
        type=str,
        help="Specify alternate bind address [default: all interfaces]",
        default="0.0.0.0",
    )
    parser.add_argument(
        "--port", type=int, help="Specify alternate port [default: 8888]", default=8888
    )
    args = parser.parse_args()

    pool = ProcessPool()

    try:
        asyncio.run(main(pool, args.host, args.port))
    except KeyboardInterrupt:
        logger.warning("\nReceived exit signal. Stopping server.")
    finally:
        pool.close()
        pool.join()
        logger.warning("Server stopped.")
