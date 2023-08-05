import os
import pandas as pd

iuye_config_path = os.getenv('iuye_config_path', 'R:\\iuye\\config')
setting_file = '%s%saccount_expense_setting.csv' % (iuye_config_path, os.sep)

df_expense_setting = pd.read_csv(setting_file)


def get_expense_setting(owner_code, broker_code, market, security_type):
    df = df_expense_setting[
        (df_expense_setting['owner_code'] == owner_code) &
        (df_expense_setting['broker_code'] == broker_code) &
        (df_expense_setting['security_type'] == security_type)
        ]
    if market is not None:
        df = df[df.market == market]
    df['expense_ratio'] = df['expense_ratio'].round(8)
    return df.to_dict(orient='records')[0]


if __name__ == '__main__':
    a = get_expense_setting('byml', 'anxin', 'SZ', 'cb')
    print(a)
    print(get_expense_setting('cexo', 'yinhe', 'SZ', 'lof'))
