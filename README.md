# x-utils

<table>
<tr>
  <td>Latest Release</td>
  <td><img src="https://img.shields.io/pypi/v/x-utils.svg" alt="latest release" /></td>
</tr>
</table>

一些常用的效用函数。

* [如何安装](https://github.com/ilampard/x-utils/blob/master/README.md#如何安装)
* [开始使用](https://github.com/ilampard/x-utils/blob/master/README.md#开始使用)
* [参考项目](https://github.com/ilampard/x-utils/blob/master/README.md#参考项目)


# 如何安装

``` python
pip install x-utils
```

# 开始使用

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





# 参考项目

[TimerTask](https://github.com/mudou192/TimerTask)

[simpleutils](https://github.com/wegamekinglc/simpleutils)