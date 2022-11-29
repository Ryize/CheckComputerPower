import multiprocessing
import threading
import time

from models import Stats


def single(func, time_start: float, stats: Stats, *args, **kwargs):
    delta = 0
    while time.time() - time_start <= stats.time:
        func(*args, **kwargs)
        stats.single = time.time() - time_start - delta
        delta = time.time() - time_start
    single = stats._single
    single["point"] = sum(single.values()) / len(single.values()) * 10000 // 1


def thread(func, time_start: float, stats: Stats, *args, **kwargs):
    while time.time() - time_start <= stats.time:
        thread = threading.Thread(
            target=_thread, args=(func, time_start, stats, *args), kwargs=kwargs
        )
        thread.start()
    while True:
        if all(list(map(lambda i: i != 0, list(stats._thread.values())))):
            thread = stats._thread
            thread["point"] = sum(thread.values()) / len(thread.values()) * 10000 // 1
            break


def _thread(func, time_start: float, stats: Stats, *args, **kwargs):
    last_index = max(stats._thread.keys(), default=0)
    stats.thread[last_index + 1] = 0
    delta = time.time()
    func(*args, **kwargs)
    stats.thread[last_index + 1] = time.time() - delta


def process(func, stats, *args, **kwargs):
    time_start = time.time()
    while time.time() - time_start <= stats._time:
        if (
                len(multiprocessing.active_children())
                < multiprocessing.cpu_count() * Stats._max_process_delta
        ):
            process = multiprocessing.Process(
                target=_process, args=(func, time_start, stats, *args), kwargs=kwargs
            )
            process.start()
            time.sleep(0.5)
    while True:
        with open("database.db", "r") as file:
            try:
                file.read().split()[-1]
            except IndexError:
                process = stats._process
                stats._process["point"] = (
                        sum(process.values()) / len(process.values()) * 10000 // 1
                )
                break


def _process(func, time_start: float, stats: Stats, *args, **kwargs):
    last_index = stats.start_process()

    delta = time.time()
    func(*args, **kwargs)
    stats.write_res_process(last_index, time.time() - delta)
