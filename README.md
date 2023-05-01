## Remote Python functions executor.

`rfunc` is a lightweight client-server application that enables running Python functions remotely as if they were executed in the local interpreter.

# Installation and examples

Install rfunc first

```
pip install -U rfunc
```

Start rfunc server (default host is 0.0.0.0 and port 8888)

```
python -mrfunc.server
```

Configure `rfunc` client from function execution side of your project:

```python
from rfunc.client import RFunc
from rfunc.client.tcp import RFuncTCPClient


remote_function = RFunc(
    client=RFuncTCPClient("127.0.0.1", 8888),
)
```

`remote_function` is a decorator which can be applied to any type of your remote function:

```python
import requests


@remote_function(
    requirements=("requests", ), # Optional list of requirements to be installed on the remote server.
    timeout=100, # Optional timeout in seconds, if the function execution exceeds this timeout, then the process on the remote server will be stopped and the connection will be terminated.
)
def fetch_http_page(host: str):
    return requests.get(host)

result = fetch_http_page("https://google.com")
print(result.status_code) # => 200
```

## Using within asyncio

`rfunc` can be useful in single-threaded asyncio applications (such as FastAPI), it allows you to move a blocking or CPU-intensive function to a process on a remote server. For example, the following code will not block the current thread:

```python
import asyncio


@remote_function()
async def counter():
    counter = 0
    while True:
        counter += 1
        if counter >= 10_000_000:
            return counter


async def another_async_func():
    while True:
        await asyncio.sleep(3)
        print("HELLO")


async def main():
    await asyncio.gather(*[counter(), another_async_func()])


if __name__ == "__main__":
    asyncio.run(main())
```
