# -*- coding: utf-8 -*-

# ref: https://github.com/mudou192/TimerTask/blob/master/manager.py



import time
from .wheel import Wheel
from ..custom_logger import CustomLogger
from ..string_utils import get_error_message


class TaskManager(object):
    def __init__(self, tasks):
        self.tasks = tasks
        self.wheel = Wheel()
        self.logger = CustomLogger(log_level='info',
                                   log_file='TaskManager.log',
                                   logger_name='TaskManager')

    def load_task(self):
        reload(self.tasks)
        for taskname in tasks.runtasks:
            if taskname not in self.tasks:
                try:
                    self.tasks[taskname] = tasks.runtasks[taskname]
                    module = __import__(taskname)
                    self.Wheel.add_task(module, taskname, **tasks.runtasks[taskname])
                except:
                    self.logger.error(get_error_message())
                time.sleep(3)
            else:
                if self.tasks[taskname] != tasks.runtasks[taskname]:
                    try:
                        self.Wheel.update_time(taskname, **tasks.runtasks[taskname])
                    except:
                        self.logger.error(get_error_message())

    def run(self):
        self.load_task()
        self.wheel.start()
        time.sleep(10)
        while 1:
            try:
                self.load_task()
            except:
                self.logger.error(get_error_message())
            time.sleep(10)


if __name__ == "__main__":
    TS = TaskManager()
    TS.run()
