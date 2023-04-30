from typing import TypedDict


class Response(TypedDict):
    requirements: tuple[str, ...]
    payload: bytes
    timeout: float
