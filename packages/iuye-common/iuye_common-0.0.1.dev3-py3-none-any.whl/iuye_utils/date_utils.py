import datetime

DEFAULT_DATE_FORMAT = '%Y%m%d'


# 获取比给定的基准日期相隔指定天数的日期
def get_diff_date(base_date: str, diff_day: int, date_format=DEFAULT_DATE_FORMAT) -> str:
    if isinstance(base_date, str):
        base_date = datetime.datetime.strptime(base_date, date_format)
    # 计算偏移量
    offset = datetime.timedelta(days=diff_day)
    # 获取想要的日期的时间
    diff_date = (base_date + offset)
    return diff_date.strftime(date_format)


def get_today_date(date_format=DEFAULT_DATE_FORMAT) -> str:
    return datetime.date.today().strftime(DEFAULT_DATE_FORMAT)


def get_week(base_date=None):
    if base_date is None:
        str_base_date = datetime.date.today().strftime('%Y-%m-%d')
        base_date = datetime.datetime.strptime(str_base_date, '%Y-%m-%d')
    elif isinstance(base_date, str):
        base_date = datetime.datetime.strptime(base_date, '%Y%m%d')
    else:
        str_base_date = base_date.strftime('%Y-%m-%d')
        base_date = datetime.datetime.strptime(str_base_date, '%Y-%m-%d')

    weekday = base_date.weekday()
    monday = base_date - datetime.timedelta(weekday)
    sunday = base_date + datetime.timedelta(6 - weekday)
    return monday, sunday


def first_day_of_year(year: int, date_format=DEFAULT_DATE_FORMAT):
    return datetime.datetime(year, 1, 1).strftime(date_format)


def last_day_of_year(year: int, date_format=DEFAULT_DATE_FORMAT):
    return datetime.datetime(year, 12, 31).strftime(date_format)


def first_day_of_quarter(year: int, quarter: int, date_format=DEFAULT_DATE_FORMAT):
    month = 3 * quarter - 2
    return datetime.datetime(year, month, 1).strftime(date_format)


def last_day_of_quarter(year: int, quarter: int, date_format=DEFAULT_DATE_FORMAT):
    if quarter == 1:
        date = datetime.datetime(year, 3, 31)
    elif quarter == 2:
        date = datetime.datetime(year, 6, 30)
    elif quarter == 3:
        date = datetime.datetime(year, 9, 30)
    elif quarter == 4:
        date = datetime.datetime(year, 12, 31)
    return date.strftime(date_format)


def first_day_of_month(year: int, month: int, date_format=DEFAULT_DATE_FORMAT):
    return datetime.datetime(year, month, 1).strftime(date_format)


def last_day_of_month(year: int, month: int, date_format=DEFAULT_DATE_FORMAT):
    if month == 2:
        date = datetime.date(year, 3, 1) - datetime.timedelta(days=1)
    elif month in (1, 3, 5, 7, 8, 10, 12):
        date = datetime.datetime(year, month, 31)
    elif month in (2, 4, 6, 9, 11):
        date = datetime.datetime(year, month, 30)
    return date.strftime(date_format)


def last_day_of_previous_month(date_format=DEFAULT_DATE_FORMAT):
    today = datetime.datetime.today()
    if today.month == 1:
        return last_day_of_month(today.year - 1, 12, date_format)
    else:
        return last_day_of_month(today.year, today.month - 1, date_format)


if __name__ == '__main__':
    print(first_day_of_year(2021))
    print(last_day_of_quarter(2021, 1))
    print(last_day_of_month(2021, 2))
    print(last_day_of_month(2000, 2))
    print(last_day_of_month(2021, 12))
    print(last_day_of_month(2021, 11))
    print(first_day_of_quarter(2021, 2))
    print(last_day_of_quarter(2021, 2))
    print(last_day_of_previous_month())
    print(last_day_of_previous_month(date_format='%Y-%m-%d'))
