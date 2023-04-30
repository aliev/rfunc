import asyncio
import socket

from .base import RFuncBaseClient


class RFuncTCPClient(RFuncBaseClient):
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    async def send_data_async(self, data: bytes) -> bytes:
        reader, writer = await asyncio.open_connection(self.host, self.port)

        writer.write(data)
        await writer.drain()

        _data = await reader.read()

        writer.close()
        await writer.wait_closed()

        return _data

    def send_data_sync(self, data: bytes) -> bytes:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(data)

            response = bytearray()

            while _data := s.recv(1024):
                response.extend(_data)

            return bytes(response)
