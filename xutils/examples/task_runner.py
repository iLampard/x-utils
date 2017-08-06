# -*- coding: utf-8 -*-


from xutils.task_runner import TaskManager

run_tasks = {
    'task0': {'interval': 3600, 'timeout': 7200},  # 每次运行完间隔3600s再次执行,默认超时时间 86400s，当timeout等于0时没有超时限制
    # 'task1': {'minute': 20},  # 每小时的20分运行
    # 'task2': {'hour': 18},  # 每天18点运行
    # 'task3': {'hour': 18, 'minute': 20},  # 每天18:20运行
    # 'task4': {'week': 3, 'hour': 18},  # 每周3的18点运行
    # 'task5': {'week': 3, 'hour': 18, 'minute': 20},  # 每周3的18:20运行
    # 'task6': {'date': 7, 'hour': 18},  # 每月7号的18点运行
    # 'task7': {'date': 7, 'hour': 18, 'minute': 20},  # 每月7号的18:20运行
}

TS = TaskManager(tasks_dict=run_tasks)
TS.run()
