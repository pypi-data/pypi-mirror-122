SOURCE_TYPE_SINA = 'sina'
SOURCE_TYPE_XUEQIU = 'xueqiu'
SOURCE_TYPE_TUSHARE_PRO = 'tushare_pro'


def security_code_to_symbol(security_code: str, source_type: str):
    """
    将证券代码转换为对应数据源所需格式的代码
    :param security_code: 证券代码
    :param source_type: 数据源类型
    :return:
    """
    if len(security_code) != 6:
        return security_code
    else:
        if security_code[:1] in ['5', '6', '9'] or security_code[:2] in ['11', '13']:
            market = 'SH'
        else:
            market = 'SZ'
        if source_type == SOURCE_TYPE_SINA:
            return market.lower() + security_code
        elif source_type == SOURCE_TYPE_XUEQIU:
            return market + security_code
        elif source_type == SOURCE_TYPE_TUSHARE_PRO:
            return '%s.%s' % (security_code, market)
        else:
            return security_code


def to_symbols(security_codes, source_type: str):
    symbols = ''
    if isinstance(security_codes, list) or isinstance(security_codes, set) or isinstance(security_codes, tuple):
        for security_code in security_codes:
            symbols += security_code_to_symbol(security_code, source_type) + ','
    else:
        symbols = security_code_to_symbol(security_codes, source_type)
    symbols = symbols[:-1] if len(symbols) > 8 else symbols
    return symbols


if __name__ == '__main__':
    print(to_symbols(['001979', '600036'], 'sina'))
