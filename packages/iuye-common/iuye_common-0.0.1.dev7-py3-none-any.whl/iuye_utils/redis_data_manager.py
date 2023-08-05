import json
import time

import pandas as pd

from iuye_utils import redis_utils as ru


class RedisDataManager:
    __redis_client_hash = {}

    USAGE_TYPE_QUOTATION = 'quotation'

    def __init__(self, usage_type):
        self.__usage_type = usage_type
        if usage_type == RedisDataManager.USAGE_TYPE_QUOTATION:
            self.__redis_client = ru.get_redis_client(db=6)
        else:
            self.__redis_client = ru.get_redis_client()

    @classmethod
    def get_instance(cls, usage_type):
        if usage_type in RedisDataManager.__redis_client_hash:
            _data_manager = RedisDataManager.__redis_client_hash[usage_type]
        else:
            _data_manager = RedisDataManager(usage_type)
            RedisDataManager.__redis_client_hash[usage_type] = _data_manager
        return _data_manager

    def save_data(self, df, key_prefix, ex=None):
        json_data = df.to_json(orient="records", force_ascii=False)
        # key_timestamp = int(time.time())
        key = '%s__%s' % (key_prefix, 'latest')
        # list_key = '%s__%s' % (key_prefix, 'list')
        self.__redis_client.set(key, json_data, ex)
        # self.__redis_client.lpush(list_key, key_timestamp)

    def load_data(self, key_prefix):
        redis_client = self.__redis_client
        # list_key = '%s__%s' % (key_prefix, 'list')
        # key_timestamp = redis_client.lindex(list_key, 0)
        # if key_timestamp is None:
        #     return None
        # key_timestamp = key_timestamp.decode()
        latest_key = '%s__%s' % (key_prefix, 'latest')
        cached_value = redis_client.get(latest_key)
        if cached_value is None:
            return None
        else:
            json_data = json.loads(redis_client.get(latest_key))
            data_list = []
            for row in json_data:
                data_list.append(row)
            return pd.DataFrame(data_list)


if __name__ == '__main__':
    data_manager = RedisDataManager.get_instance(RedisDataManager.USAGE_TYPE_QUOTATION)
    print(data_manager)
    data_manager = RedisDataManager.get_instance('abc')
    print(data_manager)
    data_manager = RedisDataManager.get_instance(RedisDataManager.USAGE_TYPE_QUOTATION)
    print(data_manager)
    pass
