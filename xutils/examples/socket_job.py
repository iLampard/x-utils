# -*- coding: utf-8 -*-

from xutils.job_runner.socket_job import SocketJob

if __name__ == '__main__':
    job = SocketJob.create_test_instance()
    job.run()
