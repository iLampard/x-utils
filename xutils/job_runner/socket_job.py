# -*- coding: utf-8 -*-


from xutils.job_runner.job import JobBase


class SocketJob(JobBase):

    @classmethod
    def meta_info(cls):
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'notes': '配置任务信息',
            'arguments': [
                # argument1
                {'type': 'dict', 'description': '在 socket_job.yaml [任务列表配置文件] 中的任务名'}

            ],
            'example_arguments': '[{\"job_name\": \"job\"}]'
        }

    def run(self):
        pass
