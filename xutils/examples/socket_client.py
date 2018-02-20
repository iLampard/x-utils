# -*- coding: utf-8 -*-

from xutils.job_runner.socket_job import SocketJob


def send_msg():
    socket_job = SocketJob(job_config='socket_job.yaml')
    socket_job.run('remote_job_1')


if __name__ == '__main__':
    send_msg()