# -*- coding: utf-8 -*-

import json
from socket import socket
from xutils.job_runner.job import JobBase
from xutils.custom_logger import CustomLogger
from xutils.decorators import handle_exception
from xutils.config_utils import find_and_parse_config

try:
    from urllib.parse import (quote,
                              unquote)
except ImportError:
    from urllib import (quote,
                        unquote)

socket_logger = CustomLogger('SocketLogger')


class SocketJob(JobBase):
    def __init__(self, job_id, execution_id, job_config='socket_job.yaml'):
        super(SocketJob, self).__init__(job_id, execution_id)
        self.job_config = job_config

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

    @classmethod
    @handle_exception(logger=socket_logger)
    def send_msg(cls, ip_address, port, msg):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip_address, port))
        client.settimeout(5)
        client.sendall(quote(msg).encode('utf-8'))

    def run(self, job_name):
        job_dict = find_and_parse_config(self.job_config)[job_name]
        socket_logger.info(job_dict)
        socket_logger.info('[%s] Now is ready to send msg.' % job_dict['name'])

        # 即将启动的任务的输入参数
        params = job_dict.get('params')
        msg = params.get('msg')

        remote_ip = job_dict.get('remote_ip')
        remote_port = job_dict.get('remote_port')
        self.send_msg(remote_ip, remote_port, json.dumps(msg))

        socket_logger.info(('[%s] Msg has been sent.' % job_name))

        return [json.dumps(job_dict)]
