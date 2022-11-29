from buisness_logic import (draw_graph, process_check, single_check,
                            thread_check)
from computer_test import process
from models import Stats


def main():
    print("Базовый тест!")
    single_check()
    print("Одноядерный тест!")
    thread_check()
    print("Многоядерный тест!")
    process(process_check, Stats())
    draw_graph(Stats())


if __name__ == "__main__":
    Stats.max_process_delta = 5
    Stats.time = 10
    Stats.mult_number = 1
    main()
