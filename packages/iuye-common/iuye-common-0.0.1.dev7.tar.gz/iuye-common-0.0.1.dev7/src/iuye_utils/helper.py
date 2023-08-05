import yaml

config_file = 'R:/iuye/config/application.yml'


def load_config():
    with open(config_file, 'rb') as f:
        config_data = yaml.safe_load(f)

    return config_data
