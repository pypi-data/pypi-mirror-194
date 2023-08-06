import threading
from betterconcurrent import Executor, ThreadPoolExecutor


class Node:
    BASE = 10
    MAX_DEPTH = 3

    def __init__(self, n, depth=0):
        self._n = n
        self._depth = depth

    def get(self):
        return self._n

    def __iter__(self):
        if self._depth >= self.MAX_DEPTH:
            return iter(tuple())

        start = self._n * self.BASE
        next_depth = self._depth + 1
        return (Node(start + i, next_depth) for i in range(self.BASE))


def search(executor: Executor, node: Node, target: int, found: threading.Event):
    if found.is_set():
        # abort: we already found the target!
        return

    if node.get() == target:
        print("found", target)
        found.set()
        return

    for child in node:
        executor.submit(search, executor, child, target, found)


def parallel_search(n: int, target: int):
    root = Node(n)
    found = threading.Event()
    with ThreadPoolExecutor(max_workers=5) as executor:
        search(executor, root, target, found)
        executor.join()

    return found.is_set()


def test_success():
    assert parallel_search(1, 115) == True


def test_failure():
    assert parallel_search(1, 215) == False


if __name__ == "__main__":
    test_success()
    test_failure()
