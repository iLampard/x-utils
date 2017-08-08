# -*- coding: utf-8 -*-

# ref: https://github.com/wegamekinglc/simpleutils/blob/master/simpleutils/testrunner.py

import os
import sys
import unittest


__all__ = ['add_parent_path', 'TestRunner']


def add_parent_path(name, level):
    current_path = os.path.abspath(name)
    sys.path.append(os.path.sep.join(current_path.split(os.path.sep)[:-level]))


class TestRunner(object):
    def __init__(self,
                 test_cases,
                 logger):
        self.suite = unittest.TestSuite()
        self.logger = logger
        for case in test_cases:
            tests = unittest.TestLoader().loadTestsFromTestCase(case)
            self.suite.addTests(tests)

    def run(self):
        self.logger.info('Python ' + sys.version)
        res = unittest.TextTestRunner(verbosity=3).run(self.suite)
        if len(res.errors) >= 1 or len(res.failures) >= 1:
            sys.exit(-1)
        else:
            sys.exit(0)
