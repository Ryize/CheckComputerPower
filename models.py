from typing import Dict


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

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance
