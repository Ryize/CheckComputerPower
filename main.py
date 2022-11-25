import multiprocessing
import threading
import time
from typing import Dict

import matplotlib.pyplot as plt


class Stats:
    _single: Dict = {}
    _thread: Dict = {}
    _process: Dict = {}
    _time: int = 5
    _max_process_delta = 4
    _mult_number = 25000

    @property
    def single(self):
        return self._single

    @single.setter
    def single(self, value):
        last_keys = max(self._single.keys(), default=0)
        self._single[int(last_keys) + 1] = value

    def get_stats(self):
        with open("database.db", "r") as file:
            process = file.read().split()
        return self.single, self._thread, process

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    def start_process(self) -> int:
        with open("database.db", "r") as file:
            last_index = len(file.read().split("\n")) - 1
        with open("database.db", "a") as file:
            file.write("0\n")
        return last_index

    def write_res_process(self, index, data):
        with open("database.db", "r") as file:
            file_data = file.read().split("\n")
        with open("database.db", "w") as file:
            file_data[index] = str(data)
            file.write("\n".join(file_data))

    @property
    def max_process_delta(self):
        return self._max_process_delta

    @max_process_delta.setter
    def max_process_delta(self, value):
        self._max_process_delta = value

    @property
    def mult_number(self):
        return self._mult_number

    @mult_number.setter
    def mult_number(self, value):
        self._mult_number = value

    @property
    def thread(self):
        return self._thread


def single(func, time_start: float, stats: Stats, *args, **kwargs):
    delta = 0
    while time.time() - time_start <= stats.time:
        func(*args, **kwargs)
        stats.single = time.time() - time_start - delta
        delta = time.time() - time_start
    single = stats._single
    single['point'] = sum(single.values()) / len(single.values()) * 10000 // 1


def thread(func, time_start: float, stats: Stats, *args, **kwargs):
    while time.time() - time_start <= stats.time:
        thread = threading.Thread(
            target=_thread, args=(func, time_start, stats, *args), kwargs=kwargs
        )
        thread.start()
    while True:
        if all(list(map(lambda i: i != 0, list(stats._thread.values())))):
            thread = stats._thread
            thread['point'] = sum(thread.values()) / len(thread.values()) * 10000 // 1
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
        if len(multiprocessing.active_children()) < multiprocessing.cpu_count() * Stats._max_process_delta:
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
                print(stats._process)
                stats._process['point'] = sum(process.values()) / len(process.values()) * 10000 // 1
                break


def _process(func, time_start: float, stats: Stats, *args, **kwargs):
    last_index = stats.start_process()

    delta = time.time()
    func(*args, **kwargs)
    stats.write_res_process(last_index, time.time() - delta)


def draw_graph(stats):
    single, thread, process = stats.get_stats()
    fig, ax = plt.subplots(3)
    fig.suptitle("Тест мощности компьютера\n")
    fig.tight_layout()

    _draw_plt(ax[0], single, 'Базовый тест')
    _draw_plt(ax[1], thread, 'Одноядерный тест')
    _draw_plt(ax[2], process, 'Многоядерный тест')

    plt.show()


def _draw_plt(ax, obj: dict, text: str):
    try:
        ax.set_title(f"{text}")
        del obj['point']
        ax.plot(list(obj.keys()), list(obj.values()))
    except (ValueError, TypeError, KeyError, AttributeError):
        pass


def timeit(mode: str = "single"):
    mode_list = {"single": single, "thread": thread, "process": process}

    def timeit_decorator(func):
        def wrapper(*args, **kwargs):
            time_start = time.time()
            stats = Stats()
            if mode in mode_list:
                mode_list.get(mode)(func, time_start, stats, *args, **kwargs)
            else:
                print("Выбран неверный режим работы!")

        return wrapper

    return timeit_decorator


@timeit("single")
def single_check():
    for i in range(Stats._mult_number):
        _ = 2 ** i


@timeit("thread")
def thread_check():
    for i in range(Stats._mult_number):
        _ = 2 ** i


def process_check():
    for i in range(Stats._mult_number):
        _ = 2 ** i


if __name__ == "__main__":
    Stats.max_process_delta = 5
    Stats.time = 10
    Stats.mult_number = 1
    print("Базовый тест!")
    single_check()
    print("Одноядерный тест!")
    thread_check()
    print("Многоядерный тест!")
    process(process_check, Stats())
    draw_graph(Stats())
