# -*- coding: utf-8 -*-


from xutils.config_utils import (merge_configs,
                                 find_and_parse_config,
                                 find_file)
from unittest import TestCase
from parameterized import parameterized
import os


class TestConfigUtils(TestCase):
    @parameterized.expand([({'a': 1, 'b': 2}, {'a': 2, 'b': 2}, {'a': 1, 'b': 2}),
                           ([['a', 1], ['b', 2], ['c', 3]], [['a', 1], ['b', 2]], [['a', 1], ['b', 2], ['c', 3]])])
    def test_merge_configs(self, to_be_merged, default, expected):
        calculated = merge_configs(to_be_merged, default)
        if isinstance(calculated, dict):
            self.assertDictEqual(calculated, expected)
        else:
            self.assertEqual(calculated, expected)

    def test_find_and_parse_config(self):
        config = find_and_parse_config('config.yaml')
        self.assertDictEqual(config, {'a': 1, 'b': 2, 'c': 3})

    def test_find_file(self):
        file = 'config_utils.py'
        path = os.path.abspath(file)
        find_path = find_file(file, path)
        self.assertEqual('xutils\\config_utils.py', find_path[-22:])

        find_path = find_file(file)
        self.assertEqual('xutils\\config_utils.py', find_path[-22:])
