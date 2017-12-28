# -*- coding: utf-8 -*-

import unittest
from parameterized import parameterized
from xutils.misc import valid_dict


class TestMisc(unittest.TestCase):
    @parameterized.expand([({'a': None, 'b': 1}, ['a'], False),
                           ({'a': None, 'b': 1}, ['b'], True),
                           ({'a': None, 'b': 1}, ['b', 'c'], False),
                           ({'a': None, 'b': 1}, None, False)])
    def test_combinations(self, d, keys, expected):
        calculated = valid_dict(d, keys)
        self.assertEqual(calculated, expected)
