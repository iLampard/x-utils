# -*- coding: utf-8 -*-


from unittest import TestCase
from parameterized import parameterized
from xutils import combinations


class TestStringUtils(TestCase):
    @parameterized.expand([(['1710', '1712'], ['.IC', '.IH'], ['1710.IC', '1710.IH', '1712.IC', '1712.IH'])])
    def test_combinations(self, list1, list2, expected):
        calculated = combinations(list1, list2)
        self.assertEqual(calculated, expected)


