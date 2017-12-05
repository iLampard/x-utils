# -*- coding: utf-8 -*-

import unittest
import copy
import tempfile
import os
import pickle
from xutils.date_utils import (Date,
                               Period,
                               Calendar)
from xutils.date_utils import (BizDayConventions,
                               Months,
                               Weekdays)


class TestCalendar(unittest.TestCase):
    def testWrongInputOfHolidayCenter(self):
        with self.assertRaises(ValueError):
            _ = Calendar('NulCalendar')

    def testCalendarConstructionIsInsensitiveOfCase(self):
        cal1 = Calendar('NullCalendar')
        cal2 = Calendar('nullcalendar')
        should_be_true = cal1 == cal2
        self.assertTrue(should_be_true)

        calto_be_different = Calendar('China.SSE')
        should_be_false = cal1 == calto_be_different
        self.assertFalse(should_be_false)

    def testBasicFunctions(self):

        test_date = Date(2015, 7, 11)
        cal = Calendar('China.SSE')
        self.assertTrue(cal.isWeekEnd(test_date.weekday()), "{0} is expected to be a weekend".format(test_date))
        test_date = Date(2015, 7, 13)
        self.assertTrue(not cal.isWeekEnd(test_date.weekday()), "{0} is expected not to be a weekend".format(test_date))

        test_date = Date(2015, 5, 29)
        cal = Calendar('China.SSE')
        self.assertTrue(cal.isEndOfMonth(test_date), "{0} is expected to be a end of month".format(test_date))

        test_date = Date(2015, 5, 1)
        cal = Calendar('China.SSE')
        end_of_month = cal.endOfMonth(test_date)
        self.assertEqual(end_of_month, Date(2015, 5, 29),
                         "The month end of 2015/5 is expected to be {0}".format(Date(2015, 5, 29)))

        biz_dates1 = cal.bizDaysBetween(Date(2015, 1, 1), Date(2015, 12, 31), True, False)
        biz_dates2 = cal.bizDaysBetween(Date(2015, 12, 31), Date(2015, 1, 1), False, True)
        self.assertEqual(biz_dates1, biz_dates2)

    def testNullCalendar(self):
        cal = Calendar("Null")

        test_date = Date(2015, 1, 1)
        self.assertTrue(cal.isBizDay(test_date))
        self.assertTrue(not cal.isHoliday(test_date))
        self.assertTrue(cal.isWeekEnd(Weekdays.Saturday))
        self.assertTrue(cal.isWeekEnd(Weekdays.Sunday))
        self.assertTrue(not cal.isWeekEnd(Weekdays.Friday))

    def testChinaSSE(self):

        expected_hol = [
            # China Shanghai Securities Exchange holiday list in the year 2014
            Date(2014, 1, 1), Date(2014, 1, 31),
            Date(2014, 2, 3), Date(2014, 2, 4), Date(2014, 2, 5), Date(2014, 2, 6),
            Date(2014, 4, 7),
            Date(2014, 5, 1), Date(2014, 5, 2),
            Date(2014, 6, 2),
            Date(2014, 9, 8),
            Date(2014, 10, 1), Date(2014, 10, 2), Date(2014, 10, 3), Date(2014, 10, 6), Date(2014, 10, 7),
            # China Shanghai Securities Exchange holiday list in the year 2015
            Date(2015, 1, 1), Date(2015, 1, 2),
            Date(2015, 2, 18), Date(2015, 2, 19), Date(2015, 2, 20), Date(2015, 2, 23), Date(2015, 2, 24),
            Date(2015, 4, 6),
            Date(2015, 5, 1),
            Date(2015, 6, 22),
            Date(2015, 9, 3), Date(2015, 9, 4),
            Date(2015, 10, 1), Date(2015, 10, 2), Date(2015, 10, 5), Date(2015, 10, 6), Date(2015, 10, 7),
            # China Shanghai Securities Exchange holiday list in the year 2016
            Date(2016, 1, 1),
            Date(2016, 2, 8), Date(2016, 2, 9), Date(2016, 2, 10), Date(2016, 2, 11), Date(2016, 2, 12),
            Date(2016, 4, 4),
            Date(2016, 5, 2),
            Date(2016, 6, 9), Date(2016, 6, 10),
            Date(2016, 9, 15), Date(2016, 9, 16),
            Date(2016, 10, 3), Date(2016, 10, 4), Date(2016, 10, 5), Date(2016, 10, 6), Date(2016, 10, 7),
            # China Shanghai Securities Exchange holiday list in the year 2017
            Date(2017, 1, 1), Date(2017, 1, 2),
            Date(2017, 1, 27), Date(2017, 1, 28), Date(2017, 1, 29), Date(2017, 1, 30), Date(2017, 1, 31),
            Date(2017, 2, 1), Date(2017, 2, 2),
            Date(2017, 4, 2), Date(2017, 4, 3), Date(2017, 4, 4),
            Date(2017, 5, 1),
            Date(2017, 5, 28), Date(2017, 5, 29), Date(2017, 5, 30),
            Date(2017, 10, 1), Date(2017, 10, 2), Date(2017, 10, 3), Date(2017, 10, 4), Date(2017, 10, 5),
            Date(2017, 10, 6), Date(2017, 10, 7), Date(2017, 10, 8),
            # China Shanghai Securities Exchange holiday list in the year 2018
            Date(2018, 1, 1),
            Date(2018, 2, 15), Date(2018, 2, 16), Date(2018, 2, 17), Date(2018, 2, 18),
            Date(2018, 2, 19), Date(2018, 2, 20), Date(2018, 2, 21),
            Date(2018, 4, 5), Date(2018, 4, 6), Date(2018, 4, 7),
            Date(2018, 4, 29), Date(2018, 4, 30), Date(2018, 5, 1),
            Date(2018, 6, 16), Date(2018, 6, 17), Date(2018, 6, 18),
            Date(2018, 9, 22), Date(2018, 9, 23), Date(2018, 9, 24),
            Date(2018, 10, 1), Date(2018, 10, 2), Date(2018, 10, 3), Date(2018, 10, 4),
            Date(2018, 10, 5), Date(2018, 10, 6), Date(2018, 10, 7)
        ]

        cal = Calendar('China.SSE')

        for day in expected_hol:
            self.assertEqual(cal.isHoliday(day), True, "{0} is expected to be a holiday in {1}".format(day, cal))
            self.assertEqual(cal.isBizDay(day), False,
                             "{0} is expected not to be a working day in {1} ".format(day, cal))

    def testChinaIB(self):

        # China Inter Bank working weekend list in the year 2014
        expected_working_week_end = [Date(2014, 1, 26),
                                     Date(2014, 2, 8),
                                     Date(2014, 5, 4),
                                     Date(2014, 9, 28),
                                     Date(2014, 10, 11),
                                     # China Inter Bank working weekend list in the year 2015
                                     Date(2015, 1, 4),
                                     Date(2015, 2, 15),
                                     Date(2015, 2, 28),
                                     Date(2015, 9, 6),
                                     Date(2015, 10, 10),
                                     # China Inter Bank working weekend list in the year 2016
                                     Date(2016, 2, 6),
                                     Date(2016, 2, 14),
                                     Date(2016, 6, 12),
                                     Date(2016, 9, 18),
                                     Date(2016, 10, 8),
                                     Date(2016, 10, 9),
                                     # China Inter Bank working weekend list in the year 2017
                                     Date(2017, 1, 22),
                                     Date(2017, 2, 4),
                                     Date(2017, 4, 1),
                                     Date(2017, 5, 27),
                                     Date(2017, 9, 30),
                                     # China Inter Bank working weekend list in the year 2018
                                     Date(2018, 2, 11),
                                     Date(2018, 2, 24),
                                     Date(2018, 4, 8),
                                     Date(2018, 4, 28),
                                     Date(2018, 9, 29),
                                     Date(2018, 9, 30)]

        cal = Calendar('China.IB')

        for day in expected_working_week_end:
            self.assertEqual(cal.isHoliday(day), False, "{0} is not expected to be a holiday in {1}".format(day, cal))
            self.assertEqual(cal.isBizDay(day), True, "{0} is expected to be a working day in {1} ".format(day, cal))

    def testAdjustDate(self):
        # April 30, 2005 is a working day under IB, but a holiday under SSE
        reference_date = Date(2005, Months.April, 30)

        sse_cal = Calendar('China.SSE')
        ib_cal = Calendar('China.IB')

        biz_day_conv = BizDayConventions.Unadjusted
        self.assertEqual(sse_cal.adjustDate(reference_date, biz_day_conv), reference_date)
        self.assertEqual(ib_cal.adjustDate(reference_date, biz_day_conv), reference_date)

        biz_day_conv = BizDayConventions.Following
        self.assertEqual(sse_cal.adjustDate(reference_date, biz_day_conv), Date(2005, Months.May, 9))
        self.assertEqual(ib_cal.adjustDate(reference_date, biz_day_conv), Date(2005, Months.April, 30))

        biz_day_conv = BizDayConventions.ModifiedFollowing
        self.assertEqual(sse_cal.adjustDate(reference_date, biz_day_conv), Date(2005, Months.April, 29))
        self.assertEqual(ib_cal.adjustDate(reference_date, biz_day_conv), Date(2005, Months.April, 30))

    def testAdvanceDate(self):
        reference_date = Date(2014, 1, 31)
        sse_cal = Calendar('China.SSE')
        ib_cal = Calendar('China.IB')

        biz_day_conv = BizDayConventions.Following

        # test null period
        self.assertEqual(sse_cal.advanceDate(reference_date, Period('0b'), biz_day_conv), Date(2014, 2, 7))

        # test negative period
        self.assertEqual(sse_cal.advanceDate(reference_date, Period('-5b'), biz_day_conv), Date(2014, 1, 24))

        # The difference is caused by Feb 8 is SSE holiday but a working day for IB market
        self.assertEqual(sse_cal.advanceDate(reference_date, Period('2b'), biz_day_conv), Date(2014, 2, 10))
        self.assertEqual(sse_cal.advanceDate(reference_date, Period('2d'), biz_day_conv), Date(2014, 2, 7))
        self.assertEqual(ib_cal.advanceDate(reference_date, Period('2b'), biz_day_conv), Date(2014, 2, 8))
        self.assertEqual(ib_cal.advanceDate(reference_date, Period('2d'), biz_day_conv), Date(2014, 2, 7))

        biz_day_conv = BizDayConventions.ModifiedFollowing
        # May 31, 2014 is a holiday
        self.assertEqual(sse_cal.advanceDate(reference_date, Period('4m'), biz_day_conv, True), Date(2014, 5, 30))

    def testDatesList(self):

        from_date = Date(2014, 1, 31)
        to_date = Date(2014, 2, 28)
        sse_cal = Calendar('China.SSE')
        ib_cal = Calendar('China.IB')

        benchmark_hol = [Date(2014, 1, 31), Date(2014, 2, 3), Date(2014, 2, 4), Date(2014, 2, 5), Date(2014, 2, 6)]
        sse_hol_list = sse_cal.holDatesList(from_date, to_date, False)
        self.assertEqual(sse_hol_list, benchmark_hol)
        ib_hol_list = ib_cal.holDatesList(from_date, to_date, False)
        self.assertEqual(ib_hol_list, benchmark_hol)

        sse_hol_list = sse_cal.holDatesList(from_date, to_date, True)
        benchmark_hol = [Date(2014, 1, 31), Date(2014, 2, 1), Date(2014, 2, 2), Date(2014, 2, 3), Date(2014, 2, 4),
                        Date(2014, 2, 5), Date(2014, 2, 6), Date(2014, 2, 8), Date(2014, 2, 9), Date(2014, 2, 15),
                        Date(2014, 2, 16), Date(2014, 2, 22), Date(2014, 2, 23)]
        self.assertEqual(sse_hol_list, benchmark_hol)
        ib_hol_list = ib_cal.holDatesList(from_date, to_date, True)
        benchmark_hol = [Date(2014, 1, 31), Date(2014, 2, 1), Date(2014, 2, 2), Date(2014, 2, 3), Date(2014, 2, 4),
                        Date(2014, 2, 5), Date(2014, 2, 6), Date(2014, 2, 9), Date(2014, 2, 15), Date(2014, 2, 16),
                        Date(2014, 2, 22), Date(2014, 2, 23)]
        self.assertEqual(ib_hol_list, benchmark_hol)

        sse_working_day_list = sse_cal.bizDatesList(from_date, to_date)
        d = from_date
        while d <= to_date:
            if sse_cal.isBizDay(d):
                self.assertTrue(d in sse_working_day_list and d not in sse_hol_list)
            d += 1

        ib_working_day_list = ib_cal.bizDatesList(from_date, to_date)
        d = from_date
        while d <= to_date:
            if ib_cal.isBizDay(d):
                self.assertTrue(d in ib_working_day_list and d not in ib_hol_list)
            d += 1

    def testCalendarWithDayConvention(self):
        sse_cal = Calendar('China.SSE')

        reference_date = Date(2015, 2, 14)
        test_date = sse_cal.adjustDate(reference_date, BizDayConventions.HalfMonthModifiedFollowing)
        self.assertEqual(test_date, Date(2015, 2, 13))

        reference_date = Date(2014, 2, 4)
        test_date = sse_cal.adjustDate(reference_date, BizDayConventions.ModifiedPreceding)
        self.assertEqual(test_date, Date(2014, 2, 7))

        reference_date = Date(2014, 2, 3)
        test_date = sse_cal.adjustDate(reference_date, BizDayConventions.Nearest)
        self.assertEqual(test_date, Date(2014, 2, 7))

        reference_date = Date(2014, 2, 2)
        test_date = sse_cal.adjustDate(reference_date, BizDayConventions.Nearest)
        self.assertEqual(test_date, Date(2014, 1, 30))

        with self.assertRaises(ValueError):
            _ = sse_cal.adjustDate(reference_date, -1)

    def testCalendarDeepCopy(self):
        sse_cal = Calendar('China.SSE')
        copied_cal = copy.deepcopy(sse_cal)

        self.assertEqual(sse_cal, copied_cal)

    def testCalendarPickle(self):
        sse_cal = Calendar('China.SSE')

        f = tempfile.NamedTemporaryFile('w+b', delete=False)
        pickle.dump(sse_cal, f)
        f.close()

        with open(f.name, 'rb') as f2:
            pickled_cal = pickle.load(f2)
            self.assertEqual(sse_cal, pickled_cal)

        os.unlink(f.name)
