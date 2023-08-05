import time

from redis import StrictRedis
from iuye_utils import config_utils

redis_config = config_utils.get_config_data('redis')
client_hash = {}


def _to_client_key(host, port, db):
    return '%s_%s_%s' % (host, port, db)


def get_redis_client(host=None, port=None, db=None):
    if host is None:
        host = redis_config['host']
    if port is None:
        port = redis_config['port']
    if db is None:
        db = redis_config['db']
    client_key = _to_client_key(host, port, db)
    if client_key in client_hash:
        _client = client_hash[client_key]
    else:
        _client = StrictRedis(host=host, port=port, db=db)
        client_hash[client_key] = _client
    return _client


def save_data(df, redis_client, index_quotation_prefix, index_quotation_list_key):
    json_data = df.to_json(orient="records", force_ascii=False)
    timestamp = int(time.time())
    key = '%s__%s' % (index_quotation_list_key, timestamp)
    redis_client.lpush(index_quotation_prefix, timestamp)
    redis_client.set(key, json_data)


def load_data():
    pass
