# -*- coding: utf-8 -*-

# ref: https://github.com/mudou192/TimerTask/blob/master/timer/timer.py

import time
import threading
from ..custom_logger import CustomLogger

MONTH_LENGTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Timer(object):
    def __init__(self, log_level, log_file):
        self.logger = CustomLogger(log_level=log_level, log_file=log_file)
        self.running = False
        # 当self.stop == True 时，该任务不再执行
        self.stop = False
        self.interval = None
        self.date = None
        self.week = None
        self.hour = 0
        self.minute = 0
        self.timeout = None
        self.runtime = 0
        self.start_time = 0

    def init_timer(self, **kwargs):
        self.interval = kwargs.get('interval')
        self.date = kwargs.get('date')
        self.week = kwargs.get('week')
        if kwargs.get('hour'):
            self.hour = kwargs.get('hour')
        if kwargs.get('minute'):
            self.minute = kwargs.get('minute')
        self.timeout = kwargs.get('timeout')
        if self.timeout is None:
            self.timeout = 86400
        self.calc_last_run_time()

    def calc_date_time(self):
        today_time = time.mktime(time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d'))
        now_month = int(time.strftime('%m'))
        now_date = int(time.strftime('%d'))
        now_hour = int(time.strftime('%H'))
        now_minute = int(time.strftime('%M'))
        if self.date < now_date and self.hour < now_hour:
            adddays = MONTH_LENGTH[now_month - 1] - (now_date - self.date)
        elif self.date == now_date and self.hour < now_hour and self.minute < now_minute:
            adddays = MONTH_LENGTH[now_month - 1]
        else:
            adddays = self.date - now_date
        return today_time + adddays * 86400 + self.hour * 3600 + self.minute * 60

    def calc_week_time(self):
        today_time = time.mktime(time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d'))
        now_week = int(time.strftime('%w'))
        now_hour = int(time.strftime('%H'))
        now_minute = int(time.strftime('%M'))
        if self.week < now_week and self.hour < now_hour:
            adddays = 7 - (now_week - self.week)
        elif self.week == now_week and self.hour < now_hour and self.minute < now_minute:
            adddays = 7
        else:
            adddays = self.week - now_week
        return today_time + adddays * 86400 + self.hour * 3600 + self.minute * 60

    def calc_hour_time(self):
        todaytime = time.mktime(time.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d'))
        nowhour = int(time.strftime('%H'))
        nowminute = int(time.strftime('%M'))
        if self.hour < nowhour:
            addhours = 24 - (nowhour - self.hour)
        elif self.hour == nowhour and self.minute < nowminute:
            addhours = 24
        else:
            addhours = self.hour - nowhour
        return todaytime + nowhour * 3600 + addhours * 3600 + self.minute * 60

    def calc_minute_time(self):
        todaytime = time.mktime(time.strptime(time.strftime('%Y-%m-%d %H'), '%Y-%m-%d %H'))
        nowminute = int(time.strftime('%M'))
        if self.minute <= nowminute:
            addminute = 60 - (nowminute - self.minute)
        else:
            addminute = self.minute - nowminute
        return todaytime + nowminute * 60 + addminute * 60

    def calc_last_run_time(self):
        """计算下一次运行的时间，在任务运行完毕或任务加载时执行"""
        nowtime = time.time()
        if self.interval and not self.runtime:
            self.runtime = nowtime
        elif self.interval and self.runtime:
            self.runtime = nowtime + self.interval
        elif self.date:
            self.runtime = self.calc_date_time()
        elif self.week:
            self.runtime = self.calc_week_time()
        elif self.hour:
            self.runtime = self.calc_hour_time()
        elif self.minute:
            self.runtime = self.calc_minute_time()
        else:
            raise Exception('wrong time format')
            # print "self.runtime:",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.runtime))

    def reload_modules(self, task_name):
        pass

    def _run(self):
        self.start_time = time.time()
        self.running = True
        self.logger.info('task starts')
        self.run()
        self.logger.info('task finishes')
        self.calc_last_run_time()
        self.running = False

    def start(self):
        task_thread = threading.Thread(target=self._run)
        task_thread.setDaemon(True)
        task_thread.start()
        time.sleep(5)

    def run(self):
        """任务运行主函数，需要自己捕捉异常，默认不会"""
        print 'do something...', time.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    T = Timer()
    T.init_timer(minute=5, hour=17, week=7)