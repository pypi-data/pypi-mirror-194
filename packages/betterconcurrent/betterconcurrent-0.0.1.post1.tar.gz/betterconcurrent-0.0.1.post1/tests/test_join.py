import threading
from betterconcurrent import Executor, ThreadPoolExecutor


class Counter:
    def __init__(self, init=0):
        self._count = init
        self._lock = threading.Lock()

    def add(self, n=1):
        with self._lock:
            self._count += n

    def read(self):
        with self._lock:
            return self._count


def countdown(executor: Executor, counter: Counter, n: int):
    if n <= 0:
        return
    counter.add(1)
    executor.submit(countdown, executor, counter, n - 1)


def test_join():
    N = 100
    with ThreadPoolExecutor(max_workers=1) as executor:
        counter = Counter()
        countdown(executor, counter, N)
        executor.join()

    val = counter.read()
    assert val == N
