# -*- coding: utf-8 -*-

# ref: https://github.com/mudou192/TimerTask/blob/master/manager.py



import time
from .wheel import Wheel
from ..custom_logger import CustomLogger
from ..string_utils import get_error_message


class TaskManager(object):
    def __init__(self, tasks_dict):
        self.tasks = {}
        self.tasks_dict = tasks_dict
        self.wheel = Wheel()
        self.logger = CustomLogger(log_level='info',
                                   log_file='TaskManager.log',
                                   logger_name='TaskManager')

    def load_task(self):
        for task_name in self.tasks_dict:
            if task_name not in self.tasks:
                self.tasks[task_name] = self.tasks_dict[task_name]
                module = __import__(task_name)
                self.wheel.add_task(module, task_name, **self.tasks_dict[task_name])
                time.sleep(3)
            else:
                if self.tasks[task_name] != self.tasks_dict[task_name]:
                    self.wheel.update_time(task_name, **self.tasks_dict[task_name])

    def run(self):
        self.load_task()
        self.wheel.start()
        time.sleep(10)
        while 1:
            self.load_task()
            time.sleep(10)


if __name__ == "__main__":
    TS = TaskManager()
    TS.run()
