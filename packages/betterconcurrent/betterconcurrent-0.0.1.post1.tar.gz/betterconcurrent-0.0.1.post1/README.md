# betterconcurrent

This is a fork of Python 3.11.2's `concurrent.futures` module, demonstrating some improvements that could be useful to merge to the standard implementation.
In short, these features are cooperative multitasking (solving the [deadlock footgun](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor)) and fire-and-forget execution of task-parallel computations.

The changes currently pertain to `ThreadPoolExecutor`. The architecture of `ProcessPoolExecutor` is not trivially amenable to these changes and is left as-is for now.

All exported types are backwards compatible and will behave the same as `concurrent.futures`, meaning that this package is a safe drop-in replacement.

You can install this package with
```
pip install betterconcurrent
```

## `Future`

Futures are now aware, through a weakref, of the executor that generated them.

### `yield_until_done`

Code running inside a function submitted to an executor can now potentially cooperatively wait for the result of a future on the same executor.
This can be done by inserting the yielding expression `yield from future.yield_until_done()`.
If the executor is capable of cooperative scheduling, the current function will be paused and its continuation will be rescheduled upon completion of the future.
If the executor does not have this capability, the call will block in the same way `future.result()` or `future.exception()` would.
In any case, `future.done()` is guaranteed to be `True` after execution resumes from the yielding expression, allowing the user to access the result without further blocking.

This introduces a new pattern for cooperative multitasking.
A top-level function `betterconcurrent.yield_until_done` accepts a list of futures and yields execution until all of them are done.

## `ThreadPoolExecutor`

### Cooperative Multitasking

`ThreadPoolExecutor` now supports cooperative multitasking and is compatible with the `yield_until_done` feature!

`concurrent.futures` code that exhibits the [deadlock footgun](https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor) can be adjusted to use this feature and never deadlock with `betterconcurrent`. Simply use `yield_until_done` before blocking on the result of any futures and execution will not stall!
It should be noted that the footgun is still present in `betterconcurrent` to maintain backward compatibility.

### Fire-and-Forget

We enable a powerful pattern wherein functions that submit subtasks without any interest in the result can be executed until convergence.

`ThreadPoolExecutor` now has a complement to `shutdown` called `join`.
Where `shutdown` would stop the computation in its tracks and prevent it from further unfolding, `join` will block until all tasks – and their subtasks – have completed, even if they continue to unfold when it is called.

#### Example

A search for a particular node in a tree can be parallelized by recursively spawning a subtask for each of the children. We might not care to return the value to the caller, but rather print a message or assign the result to a shared variable.
See [tree_search.py](tests/test_tree_search.py) for an example of a parallel tree search!

## To do

- [ ] Achieve full exception-safety. Some unlucky exception firings might cause undefined behavior currently.
