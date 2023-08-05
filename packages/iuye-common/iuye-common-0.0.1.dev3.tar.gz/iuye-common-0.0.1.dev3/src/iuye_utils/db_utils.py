from iuye_utils import config_utils
from sqlalchemy import create_engine

mysql_config = config_utils.get_config_data('mysql')


def get_connection(db_name):
    db_url = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
        mysql_config['username'], mysql_config['password'], mysql_config['ip'], mysql_config['port'], db_name)
    engine = create_engine(db_url, encoding='utf-8')
    return engine


def get_table_names(db_name):
    engine = get_connection(db_name)
    return engine.table_names()


if __name__ == '__main__':
    tn = get_table_names('jisilu_data')
    print(tn)
