import datetime

import arrow
import math

TIMEZONE = 'Asia/Shanghai'

DATETIME_FORMAT = 'YYYY-MM-DD HH:mm:ss'
NORMAL_DATE_FORMAT = 'YYYY-MM-DD'


def get_date_between(start_date, end_date):
    """
    获取两个日期之间相隔多少天
    """

    date_delta = end_date - start_date
    date_between = int(math.fabs(date_delta.days))
    return date_between


def get_weeks_between(start_date, end_date):
    """
    获取两个日期之间相隔多少天
    datetime 类型加上 .date 获取日期
    """
    week_start = start_date - datetime.timedelta(days=start_date.weekday())
    week_end = end_date - datetime.timedelta(days=end_date.weekday())
    return (week_end - week_start).days // 7


def compare_two_date(first, last, fmt='YYYY-MM-DD'):
    """
    两个时间比较

    first_date < last_date : < 0
    first_date > last_date : > 0
    first_date = last_date : = 0
    """
    first_date = arrow.get(first)
    last_date = arrow.get(last)

    if first_date > last_date:
        return 1
    elif first_date < last_date:
        return -1
    else:
        return 0


def get_date_by_fmt(*args, **kwargs):
    return arrow.get(*args, **kwargs).replace(tzinfo=TIMEZONE)


def get_date(date=None):
    return arrow.get(date).replace(tzinfo=TIMEZONE)


def get_date_start_end(date):
    day_start_end = date.span('day')
    day_start = day_start_end[0]
    day_end = day_start_end[1]
    return day_start, day_end


def whether_date_in_date_between(start, end, date):
    """
    某个日期是否在某两个确切的日期区间内
    """
    _start = get_date(start)
    _end = get_date(end)
    _date = get_date(date)

    if not _start <= _end:
        raise AttributeError('start_date must smaller than end_date')

    return _start <= _date <= _end


def get_current_hours(hour=+0, fmt='YYYY-MM-DD HH:mm:ss'):
    """
    获取当前时间并根据hour做调整
    :param fmt:
    :param hour:
    :return:
    """
    return arrow.now().replace(hours=hour).format(fmt=fmt)


def format_date(date, fmt=DATETIME_FORMAT) -> object:
    """
    格式化时间
    :param date:  'YYYY-MM-DD' or datetime or '2018-12-19T09:29:00' else
    :param fmt:
    :return:
    """
    return get_date(date).format(fmt=fmt)


def get_now():
    """
    获取当前时间
    :return:  arrow
    """
    return arrow.now()


def replace_day(date, days=+0, fmt='YYYY-MM-DD'):
    """
    获取当前时间并根据days做调整, 默认为当天
    days: +1, -1
    """
    if not date:
        date = arrow.now()
    return get_date(date).replace(days=days).format(fmt)


def time_to_datetime(hour, minute, second):
    """将time类型转datetime"""
    return datetime.datetime.now().replace(hour=hour, minute=minute, second=second)


def get_date_floor(date, frame='day'):
    """
    获取时间的底
    :param date:
    :param frame: day/hour
    :return:
    """
    return get_date(date).floor(frame)


def get_date_ceil(date, frame='day'):
    """
    获取时间的顶
    :param date:
    :param frame: day/hour
    :return:
    """
    return get_date(date).ceil(frame)


def shift_month_date(months=-0, fmt='YYYY-MM-DD'):
    """
    偏移时间-按月来偏移
    :return:
    """
    return get_date().shift(months=months).format(fmt)


def sec_to_str(param):
    """
    秒转为时分秒字符串
    """
    m, s = divmod(param, 60)
    h, m = divmod(m, 60)
    if h >= 24:
        h -= 24
    return "%02d:%02d:%02d" % (h, m, s)


def str_to_sec(param):
    """
    字符串时分秒转换成秒
    """
    h, m, s = param.strip().split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def time_to_sec(y):
    """
    时间类型时分秒转换成秒
    """
    h = y.hour  # 直接用datetime.time模块内置的方法，得到时、分、秒
    m = y.minute
    s = y.second
    return int(h) * 3600 + int(m) * 60 + int(s)  # int()函数转换成整数运算


def sec_to_time(seconds):
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"%02d:%02d:%02d" % (h, m, s)


def get_current_timestamp():
    return str(get_now().timestamp)


def get_now_weekday():
    """
    用于外卖的 weekday
    """
    weekday = get_now().weekday()
    if 4 <= get_now().hour < 10:  # 4:00 - 9:59
        hour = 0
    elif 10 <= get_now().hour < 15:  # 10:00 - 14:59
        hour = 1
    elif 15 <= get_now().hour < 20:  # 15:00 - 20:00
        hour = 2
    else:  # 20:00 - 3:59
        hour = 3
    return 1 << (weekday * 4 + hour)


def get_date_remain(start_date, end_date):
    """
    获取剩余剩余的时间

    eg:
        start_date = '2019-03-03',  end_date = '2020-02-02' return (336, 0, 0, 0)
        start_date = '2020-03-25 05:33:23',  end_date = '2020-03-26 12:40:13' return (1, 7, 6, 50)
        start_date = '2020-03-26 05:33:23',  end_date = '2020-03-26 12:40:13' return (0, 7, 6, 50)
    """
    start = get_date(start_date)
    end = get_date(end_date)
    delta = end - start

    days = delta.days  # 剩余天数
    hours, remainder = divmod(delta.seconds, 3600)  # 剩余小时数
    minutes, seconds = divmod(remainder, 60)  # 获取剩余小时

    return days, hours, minutes, seconds


def get_datetime(date, fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(date, fmt)


def get_date_range(date, frame='day'):
    """
    返回当日时间低和定的时间范围,用于orm range条件
    :param date:
    :return:
    """
    return (format_date(get_date_floor(date, frame)), format_date(get_date_ceil(date, frame)))


def get_every_day(begin_date, end_date):
    """
    获得两个日期中所有有效日期
    """
    date_list = []
    # begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    # end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


def get_time_between(start_time, end_time):
    """判断现在是否在这两个时间内"""
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + str(start_time), '%Y-%m-%d%H:%M:%S')
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + str(end_time), '%Y-%m-%d%H:%M:%S')
    now_time = datetime.datetime.now()
    if now_time > start_time and now_time < end_time:
        return True
    return False

def get_current_week():
    """获得今天星期几"""
    return datetime.datetime.today().isoweekday()

def get_current_date():
    """获得今天日期"""
    return datetime.datetime.now().strftime('%Y-%m-%d')


def calculate_age(birth):
    """计算年龄，少于1岁用日差除以365计算"""
    birth_d = birth
    today_d = datetime.datetime.now()
    if today_d.month > birth_d.month:
        age = today_d.year - birth_d.year
    else:
        age = today_d.year - birth_d.year - 1

    if age <= 0:
        date_between = get_date_between(birth_d, today_d)
        age = round(date_between / 365, 2)
    return age
