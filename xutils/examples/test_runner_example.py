# -*- coding: utf-8 -*-


from unittest import TestCase
from xutils import (CustomLogger,
                    TestRunner)


class Test1(TestCase):
    def test_1(self):
        self.assertEqual([1.0, 2.0], [1.0, 2.0])


class Test2(TestCase):
    def test_2(self):
        self.assertEqual(1.0 * 3, 3.0)


if __name__ == '__main__':
    test_runner_logger = CustomLogger(logger_name='TestRunner')
    runner = TestRunner([Test1, Test2],
                        test_runner_logger)
    runner.run()
