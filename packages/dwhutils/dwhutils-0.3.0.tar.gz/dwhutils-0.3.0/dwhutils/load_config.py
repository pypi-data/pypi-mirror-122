import os

import yaml

home = os.path.expanduser('~')
cpath = os.path.join(home, ".dwh", "dwh_config.yaml")


def get_db_config():
    with open(cpath) as file:
        config = yaml.full_load(file)
    return config['db_config']


def get_keypass_config():
    with open(cpath) as file:
        config = yaml.full_load(file)
    return config['keypass']


def get_entity_configs():
    with open(cpath) as file:
        config = yaml.full_load(file)
    return config['entity_configs']


def get_data_path_config():
    with open(cpath) as file:
        config = yaml.full_load(file)
    return config['data_path']
