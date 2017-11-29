# -*- coding: utf-8 -*-


from xutils import (Date,
                    Period,
                    Calendar,
                    Schedule)

# 生成Date对象
current_date = Date(2015, 7, 24)

# Date对象的字符串表示
str(current_date)  # 2015-07-24

# 也可以直接传递5位数的序列号初始化Date对象
current_date_2 = Date(serialNumber=current_date.serialNumber)
str(current_date_2)  # 2015-07-24

# Date对象转换成datetime格式
current_date.toDateTime()  # dt.datetime(2015, 7, 24)

# 从字符串初始化成Date对象
Date.parseISO('2016-01-15')
Date.strptime('20160115', '%Y%m%d')

# Date对象的加减
Date()

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
cal.advanceDate(current_date, Period('-5b'))  # Date(2014, 1, 24)
# 当前日往后推4个月
cal.advanceDate(current_date, Period('4m'))  # Date(2014, 6, 3)

# 日期的加减
# 一个月后的日期
print(current_date + '1M')
print(current_date + Period('1M'))
