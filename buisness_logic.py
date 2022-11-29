import time

from matplotlib import pyplot as plt

from computer_test import process, single, thread
from models import Stats


def draw_graph(stats):
    single, thread, process = stats.get_stats()
    fig, ax = plt.subplots(3)
    fig.suptitle("Тест мощности компьютера\n")
    fig.tight_layout()

    _draw_plt(ax[0], single, "Базовый тест")
    _draw_plt(ax[1], thread, "Одноядерный тест")
    _draw_plt(ax[2], process, "Многоядерный тест")

    plt.show()


def _draw_plt(ax, obj: dict, text: str):
    try:
        ax.set_title(f"{text}")
        del obj["point"]
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
        _ = 2**i


@timeit("thread")
def thread_check():
    for i in range(Stats._mult_number):
        _ = 2**i


def process_check():
    for i in range(Stats._mult_number):
        _ = 2**i
