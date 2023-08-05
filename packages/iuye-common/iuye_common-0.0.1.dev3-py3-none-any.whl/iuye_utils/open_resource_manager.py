import os

import yaml

yamlPath = 'R:/config/open_resource.yml'

with open(yamlPath, 'rb') as f:
    open_resource_config = yaml.safe_load(f)


def load_config():
    pass


def get_data_path(resource_type, relative_path=None):
    special_config = open_resource_config[resource_type]
    data_path = special_config['data_path']
    if relative_path is not None:
        data_path = '%s/%s' % (data_path, relative_path.lstrip('/'))

    if not os.path.exists(data_path):
        os.makedirs(data_path)
    return data_path


if __name__ == '__main__':
    s = get_data_path('jisilu', '/lof')
    print(s)
