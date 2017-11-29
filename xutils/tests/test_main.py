# -*- coding: utf-8 -*-

import os
import sys

thisFilePath = os.path.abspath(__file__)
sys.path.append(os.path.sep.join(thisFilePath.split(os.path.sep)[:-3]))

from xutils import (CustomLogger,
                    TestRunner)
from xutils.tests.test_assert import TestAssert
from xutils.tests.test_date import TestDate
from xutils.tests.test_calendar import TestCalendar
from xutils.tests.test_schedule import TestSchedule
from xutils.tests.test_period import TestPeriod
from xutils.tests.test_config_utils import TestConfigUtils
from xutils.tests.test_string_utils import TestStringUtils

if __name__ == '__main__':
    test_logger = CustomLogger('TestLogger')
    test_runner = TestRunner([TestAssert,
                              TestDate,
                              TestCalendar,
                              TestSchedule,
                              TestPeriod,
                              TestConfigUtils,
                              TestStringUtils],
                             test_logger)
    test_runner.run()
