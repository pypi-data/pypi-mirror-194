from betterconcurrent import ThreadPoolExecutor, yield_until_done


def wait_on_future(executor):
    fs = [executor.submit(pow, 5, i) for i in range(2, 10)]
    yield from yield_until_done(fs)
    return [f.result() for f in fs]


def test_multiple_continuations():
    with ThreadPoolExecutor(max_workers=1) as executor:
        f = executor.submit(wait_on_future, executor)
        assert f.result() == [25, 125, 625, 3125, 15625, 78125, 390625, 1953125]
        executor.join()
