# x-utils

<table>
<tr>
  <td>Python version</td>
  <td><img src="https://img.shields.io/badge/python-2.7-blue.svg"/>   <img src="https://img.shields.io/badge/python-3.5-blue.svg"/>  <img src="https://img.shields.io/badge/python-3.6-blue.svg"/> </td>
  </tr>

<tr>
<tr>
  <td>Latest Release</td>
  <td><img src="https://img.shields.io/pypi/v/x-utils.svg" alt="latest release" /></td>
</tr>

<tr>
  <td>Build Status</td>
  <td><img src="https://travis-ci.org/iLampard/x-utils.svg?branch=master" alt="build status" /></td>
</tr>

</table>



一些常用的效用函数。

* [如何安装](https://github.com/ilampard/x-utils/blob/master/README.md#如何安装)
* [开始使用](https://github.com/ilampard/x-utils/blob/master/README.md#开始使用)
    * 日期工具函数(该部分参考了[finance-python](https://github.com/alpha-miner/Finance-Python))
        * Date: 将datetime或者字符串格式的日期转换为*Date*类型，提供各种效用函数方便进行格式转换和日期加减、调整等
        * Calendar: 预定义了上交所、银行间两个中国交易日历，可供日期加减、调整时使用
        * Period: 可用字符串形式初始化*Period*对象，定义一个时间周期，传递给*Date／Calendar／Schedule* 对象使用
        * Schedule：可结合*Date／Calendar／Period* 定义循环往复的日程表
        上述四个类的对象可混合使用。
    * 日志工具: CustomLogger
    * 单元测试合集：TestRunner(参考了[simpleutils](https://github.com/wegamekinglc/simpleutils)) 
    * 常用装饰器 
        * 计时器： clock
        * 异常处理: handle_exception
        * 装饰器与日志的结合使用
    * YAML配置文件的解析：find_and_parse_config 
* [参考项目](https://github.com/ilampard/x-utils/blob/master/README.md#参考项目)


# 如何安装

``` python
pip install x-utils
```

# 开始使用
##### Date Utilities

###### Date
```python

from xutils import (Date,
                    Period)

# 生成Date对象
current_date = Date(2015, 7, 24)

# Date对象的字符串表示
str(current_date)  
>>>2015-07-24

# 也可以直接传递5位数的序列号初始化Date对象
current_date_2 = Date(serialNumber=current_date.serialNumber)
str(current_date_2)  
>>>2015-07-24

# Date对象转换成datetime格式
current_date.toDateTime()  
>>>dt.datetime(2015, 7, 24)

# 从字符串初始化成Date对象
Date.parseISO('2016-01-15')
Date.strptime('20160115', '%Y%m%d')
>>>Date(2016, 1, 15)

# 日期的加减 (不考虑交易日的情况)
# 一个月后的日期
current_date + '1M'
current_date + Period('1M') # 与上一行结果相同

```


###### Calendar / Period

```python

from xutils import (Date, 
                    Calendar,
                    Period)

# 设定为上交所的交易日历
cal = Calendar('China.SSE')

# 假设某日为 2015-07-11(周六), 初始化一个Date对象
current_date = Date(2015, 7, 11)

# 判断该日是否是交易日、节假日、周末或者月末
cal.isBizDay(current_date)  # False
cal.isHoliday(current_date)  # True
cal.isWeekEnd(current_date.weekday())  # True
cal.isEndOfMonth(current_date)  # False

# 交易日历下的日期加减

# 默认 当计算返回值为非交易日时返回下一个交易日 bizDayConv = BizDayConventions.Following
current_date = Date(2014, 1, 31)

# 当前日往前推五个交易日
cal.advanceDate(current_date, Period('-5b'))  
>>>Date(2014, 1, 24)

# 当前日往后推4个月
cal.advanceDate(current_date, Period('4m')) 
>>>Date(2014, 6, 3)


```

###### Schedule

```python

from xutils import (Date, 
                    Period,
                    Calendar,
                    Schedule,
                    TimeUnits,
                    BizDayConventions)

# Jan 2 and Jan 3 are skipped as New Year holiday
# Jan 7 is skipped as weekend
# Jan 8 is adjusted to Jan 9 with following convention
start_date = Date(2012, 1, 1)
s = Schedule(start_date,
             start_date + 7,
             Period(length=1, units=TimeUnits.Days),
             Calendar('China.SSE'),
             BizDayConventions.Preceding)
>>>
[Date(2011, 12, 30), Date(2012, 1, 4), Date(2012, 1, 5), Date(2012, 1, 6), Date(2012, 1, 9)]

```


##### CustomLogger


*CustomLogger *在* logging* 的基础上丰富了功能，可一次性自定义名称 *logger_name*，级别 *log_level*以及输出的*log_file*(可选)
- *set_level* 方法可控制*log_level*，以决定信息的级别
- 例子可具体参见[CustomLogger](https://github.com/iLampard/x-utils/blob/master/xutils/examples/logger.py)
```python

from xutils.custom_logger import CustomLogger

LOGGER = CustomLogger(logger_name='TestLogger', log_level='info', log_file='test.log')
LOGGER.info('Hello world')
LOGGER.set_level('critical')
LOGGER.info('Hello world')

>>>
[2017-08-08 10:07:34 - TestLogger - INFO] - Hello world

```

##### clock
*clock* 提供了方便的函数计时器功能

```python
from xutils.decorators import clock
from xutils.custom_logger import CustomLogger

LOGGER = CustomLogger(logger_name='TestLogger', log_level='info', log_file='clock.log')


@clock(LOGGER)
def test_calc():
    sum = 0
    for i in range(100000):
        sum += i
    return


test_calc()
>>>
[2017-09-06 14:57:38 - TestLogger - INFO] - function test_calc used : 0.00600004196167 s
```

##### TestRunner

*TestRunner* 主要是为了方便建立单元测试集合*TestSuite*

```python

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


```

##### handle_exception 与 CustomLogger 结合使用



```python
from xutils.custom_logger import CustomLogger
from xutils.decorators import handle_exception

LOGGER = CustomLogger(logger_name='TestLogger', log_level='info', log_file='test.log')


@handle_exception(logger=LOGGER)
def test_exception():
    raise ValueError('Error here blabla')


if __name__ == '__main__':
    test_exception()

```


#### config utility
*find_file* 根据给定开始搜索的地址，逐步往根目录回滚搜索目标文件

```python

# xutils/tests/test_config_utils.py
find_path = find_file(target_file='config_utils.py')

>>> 'xutils\\config_utils.py'


```


*find_and_parse_config* 的功能是读取给定yaml配置文件中的信息，如果有默认配置文件，那么将二者读取的信息合并（如果信息有重复，则以给定配置文件信息为准）。
```python

# xutils/tests/test_config_utils.py
find_and_parse_config('config.yaml')

>>> {'a': 1, 'b': 2, 'c': 3}


```



# 参考项目

[TimerTask](https://github.com/mudou192/TimerTask)

[simpleutils](https://github.com/wegamekinglc/simpleutils)

[finance-python](https://github.com/alpha-miner/Finance-Python)