from pymongo import MongoClient

from iuye_utils import config_utils as cu

config_data = cu.get_config_data('mongo')


def _to_client_key(host, port, db):
    return '%s_%s_%s' % (host, port, db)


if 'username' in config_data:
    _client = MongoClient(
        host=config_data['host'],
        port=config_data['port'],
        username=config_data['username'],
        password=config_data['password'])
else:
    _client = MongoClient(
        host=config_data['host'],
        port=config_data['port'])


def get_client():
    return _client


def get_database(db_name):
    return get_client()[db_name]


def get_db_collection(db_name, collection_name):
    return get_database(db_name)[collection_name]


if __name__ == '__main__':
    client = get_client()
    db = client['test_01']
    collection = db['stock_basic']
    collection.insert_one({'a': 1, 'b': 2})
    client.drop_database('test_01')
