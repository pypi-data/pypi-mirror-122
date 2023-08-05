def _get_seconds(hour, start_minute, end_minute, seconds_interval=1):
    _time_list = []
    s1 = '%02d:%02d:%02d'
    for minute in range(start_minute, end_minute):
        for second in range(0, 60, seconds_interval):
            _time_list.append(s1 % (hour, minute, second))
    return _time_list


def get_continuous_auction_seconds(seconds_interval=1):
    """
    获取集合竞价时段的整秒时刻列表
    :return:
    """
    _time_list = []
    _time_list = _time_list + _get_seconds(9, 25, 29, seconds_interval)
    _time_list = _time_list + _get_seconds(9, 30, 60, seconds_interval)
    _time_list = _time_list + _get_seconds(10, 0, 60, seconds_interval)
    _time_list = _time_list + _get_seconds(11, 0, 35, seconds_interval)

    _time_list = _time_list + _get_seconds(13, 0, 60, seconds_interval)
    _time_list = _time_list + _get_seconds(14, 0, 57, seconds_interval)
    _time_list = _time_list + _get_seconds(15, 0, 10, seconds_interval)

    # _time_list.remove('14:57:00')

    # TODO
    # _time_list = _time_list + _get_seconds(17, 0, 60, seconds_interval)
    return _time_list


# aggregated auction 集合竞价

if __name__ == '__main__':
    trade_seconds = get_continuous_auction_seconds()
    print(trade_seconds)
