import time
import uuid
import datetime as dt
from typing import Optional

from dataengtoolbox.utils import hello, timeit
from dataengtoolbox.version import version


# Command Line Interface
class CLI:

    def __init__(self):
        self.version = version
        self.execution_timestamp = dt.datetime.utcnow()
        self.execution_id = str(uuid.uuid4())

    def hello(self, name: Optional[str] = None):
        return hello(name=name)

    def add(self, *args) -> int:
        return sum(args)

    @timeit
    def sleep(self, duration: int = 3):
        time.sleep(duration)

    @staticmethod
    def square(num: int) -> int:
        return num ** 2
