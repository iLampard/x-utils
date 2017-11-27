# -*- coding: utf-8 -*-


import unittest
import warnings
from xutils import (py_assert,
                    py_warning)


class TestAssert(unittest.TestCase):
    def test_py_assert(self):
        with self.assertRaises(ValueError):
            py_assert(1 == 2, ValueError)

    def test_py_warning(self):
        with warnings.catch_warnings(record=True) as warnings_list:
            warnings.simplefilter('always')
            py_warning(1 == 2, DeprecationWarning)
            self.assertTrue(any(item.category == DeprecationWarning for item in warnings_list))
