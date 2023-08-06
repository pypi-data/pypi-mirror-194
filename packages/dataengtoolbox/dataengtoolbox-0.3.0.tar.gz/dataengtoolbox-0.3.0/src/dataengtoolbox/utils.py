import datetime as dt
from typing import Optional

from dataengtoolbox.settings import DEFAULT_HELLO_NAME


def hello(name: Optional[str] = None) -> str:
    name = name or DEFAULT_HELLO_NAME
    return f"Hello, {name}!"


def timeit(fun):
    def wrapper(*args, **kwargs):
        start = dt.datetime.utcnow()
        output = fun(*args, **kwargs)
        seconds = (dt.datetime.utcnow() - start).seconds
        return {
            "execution_timestamp_start": start.strftime("%Y-%m-%d"),
            "execution_duration_in_seconds": seconds,
            "output": output
        }
    return wrapper
