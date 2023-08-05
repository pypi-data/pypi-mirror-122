import os

import yaml

iuye_config_path = os.getenv('iuye_config_path', 'R:\\iuye\\config')
default_yaml_file_path = '%s%sapplication.yml' % (iuye_config_path, os.sep)
with open(default_yaml_file_path, 'rb') as f:
    _config_data = yaml.safe_load(f)


def get_config_data(key=None):
    if key is None:
        return _config_data
    else:
        return _config_data[key]
