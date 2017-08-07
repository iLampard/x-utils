# -*- coding: utf-8 -*-


from xutils.task_runner import Timer


class TaskServer(Timer):
    def __init__(self, **kwargs):
        log_level = kwargs.get('log_level', 'info')
        log_file = kwargs.get('log_file', __file__ + '.log')
        super(TaskServer, self).__init__(log_level, log_file)

    def TaskServer(self):
        print 'hello world'
