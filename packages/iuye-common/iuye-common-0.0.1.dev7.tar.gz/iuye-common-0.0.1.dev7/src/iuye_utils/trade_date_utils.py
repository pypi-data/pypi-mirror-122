import datetime

import pandas as pd
from iuye_utils import db_utils


class TradeDateUtils:
    conn = db_utils.get_connection('open_finance_data')
    sql = "SELECT cal_date FROM tushare_pro_trade_cal WHERE exchange = 'SSE' AND is_open = 1 ORDER BY cal_date DESC"
    df = pd.read_sql(sql, conn)
    trade_date_list = list(df['cal_date'])
    trade_date_list.reverse()

    @classmethod
    def is_trade_date(cls, base_date: str):
        return pd.to_datetime(base_date).strftime('%Y%m%d') in cls.trade_date_list

    @classmethod
    # 获取比给定的基准日期相隔指定天数的交易日
    def get_diff_date(cls, base_date: str, diff_day: int):
        trade_date_list = cls.trade_date_list
        current_base_date = pd.to_datetime(base_date).strftime('%Y%m%d')

        if current_base_date not in trade_date_list:
            sql = "SELECT cal_date FROM tushare_pro_trade_cal WHERE exchange = 'SSE' AND" \
                  " is_open = 1 AND cal_date >= %s ORDER BY cal_date ASC LIMIT 1"
            cur = cls.conn.execute(sql, current_base_date)
            current_base_date = cur.fetchone()[0]

        index = trade_date_list.index(current_base_date)
        return pd.to_datetime(trade_date_list[index + diff_day])

    @classmethod
    def get_latest_trade_date(cls, base_date: str = None):
        if base_date is None:
            latest_base_date = datetime.datetime.today().strftime('%Y%m%d')
        else:
            latest_base_date = pd.to_datetime(base_date).strftime('%Y%m%d')

        trade_date_list = cls.trade_date_list

        if latest_base_date not in trade_date_list:
            sql = "SELECT cal_date FROM tushare_pro_trade_cal WHERE exchange = 'SSE' AND" \
                  " is_open = 1 AND cal_date <= %s ORDER BY cal_date DESC LIMIT 1"
            cur = cls.conn.execute(sql, latest_base_date)
            latest_base_date = cur.fetchone()[0]

        return pd.to_datetime(latest_base_date)

    
    @classmethod
    def get_current_or_next_trade_date(cls, base_date: str):
        latest_base_date = pd.to_datetime(base_date).strftime('%Y%m%d')
        trade_date_list = cls.trade_date_list

        if latest_base_date not in trade_date_list:
            sql = "SELECT cal_date FROM tushare_pro_trade_cal WHERE exchange = 'SSE' AND" \
                  " is_open = 1 AND cal_date >= %s ORDER BY cal_date ASC LIMIT 1"
            cur = cls.conn.execute(sql, latest_base_date)
            latest_base_date = cur.fetchone()[0]

        return pd.to_datetime(latest_base_date)

    @classmethod
    def get_previous_trade_date(cls, base_date: str = None):
        latest_trade_date = cls.get_latest_trade_date(base_date)
        pre_trade_date = cls.get_diff_date(latest_trade_date, -1)
        return pd.to_datetime(pre_trade_date)


if __name__ == '__main__':
    print(TradeDateUtils.get_latest_trade_date())
    print(TradeDateUtils.get_diff_date('20200716', -3))
    print(TradeDateUtils.get_diff_date('2020-7-18', -5))
    print(TradeDateUtils.get_diff_date('2020-8-29', 0))
    print(TradeDateUtils.get_diff_date('2020-8-29', 3))
    print(TradeDateUtils.get_diff_date('2020-10-11', 1))
    print(TradeDateUtils.get_diff_date('2020-10-8', 1))
    print(TradeDateUtils.get_diff_date('2020-12-28', 5))
    print(TradeDateUtils.get_previous_trade_date('2021-2-28'))
