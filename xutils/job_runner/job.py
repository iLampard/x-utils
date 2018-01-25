# -*- coding: utf-8 -*-

import os
import socket


# ref: https://github.com/Nextdoor/ndscheduler/blob/master/ndscheduler/job.py

class JobBase(object):
    def __init__(self):
        pass

    @classmethod
    def create_test_instance(cls):
        """Creates an instance of this class for testing."""
        return cls(None, None)

    @classmethod
    def get_job_description(cls):
        hostname = socket.gethostname()
        pid = os.getpid()
        return 'hostname: {0} | pid: {1}'.format(hostname, pid)

    @classmethod
    def meta_info(cls):
        """Returns meta info for this job class.
        For example:
            {
                'job_class_string': 'myscheduler.jobs.myjob.MyJob',
                'arguments': [
                    {'type': 'string', 'description': 'name of this channel'},
                    {'type': 'string', 'description': 'what this channel does'},
                    {'type': 'int', 'description': 'created year'}
                ],
                'example_arguments': '["music channel", "it's an awesome channel", 1997]',
                'notes': 'need to specify environment variable API_KEY first'
            }
        The arguments property should be consistent with the run() method.
        This info will be used in web ui for explaining what kind of arguments is needed for a job.
        You should override this function if you want to make your scheduler web ui informative :)
        :return: meta info for this job class.
        :rtype: dict
        """
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'arguments': [],
            'example_arguments': '',
            'notes': ''
        }

    def run(self, *args, **kwargs):
        """The "main" function for a job.
        Any subclass has to implement this function.
        The return value of this function will be stored in the database as json formatted string
        and will be shown for each execution in web ui.
        :param args:
        :param kwargs:
        :return: None or json serializable object.
        """
        raise NotImplementedError('Please implement this function')
