import os
from collections.abc import Mapping

import yaml

from .functions import log

DEFAULT_GLOBAL_CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/default_global_configs.yml'
DEFAULT_GUILD_CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/default_guild_configs.yml'


def load_configs(*, global_path='global_configs.yml', guild_dir='configs/'):
    # Global Configuration File
    try:
        default_global_configs = yaml.safe_load(open(DEFAULT_GLOBAL_CONFIG_PATH, encoding='UTF-8'))
    except FileNotFoundError as e:
        log(f'{e} \nCould not find default Global Configuration File.', tag='Critical')
        raise

    global_config_path = os.getcwd() + '/' + global_path
    try:
        global_configs = yaml.safe_load(open(global_config_path, encoding='UTF-8'))
    except FileNotFoundError:
        log(f'Did not find Global Configuration File at {global_config_path}; using Defaults.', tag='Info')
        raise
    else:
        _recursive_merge(default_global_configs, global_configs)

    # Guild Configuration Files
    try:
        default_guild_configs = yaml.safe_load(open(DEFAULT_GUILD_CONFIG_PATH, encoding='UTF-8'))
    except FileNotFoundError as e:
        log(f'{e} \nCould not find default Guild Configuration File.', tag='Critical')
        raise

    guild_prefixes, guild_configs = {}, {}
    guild_configs_dir = os.getcwd() + '/' + guild_dir
    for file in os.listdir(guild_configs_dir):
        file_name = os.path.basename(file).rpartition('.')
        if file_name[-1] != 'yml':
            continue

        config_file = yaml.safe_load(open(guild_configs_dir + file))
        _recursive_merge(default_guild_configs, config_file)

        guild_id = int(config_file['guild']['id'])
        if int(file_name[0]) != guild_id:
            log(f'Mismatched file name ID and Guild ID in file: {file}', tag='Critical')
            raise

        guild_prefixes[guild_id] = config_file['bot']['prefix']
        guild_configs[guild_id] = config_file

    return global_configs, guild_configs, guild_prefixes


def _recursive_merge(old, new):
    for k, v in new.items():
        if k in old and isinstance(old[k], dict) and isinstance(new[k], Mapping):
            _recursive_merge(old[k], new[k])
        else:
            old[k] = new[k]


def save_guild_config(config, guild_id):
    guild_configs_dir = os.getcwd() + '/configs/'
    with open(f'{guild_configs_dir}{guild_id}.yml', mode='w', encoding='UTF-8') as config_file:
        yaml.safe_dump(config, config_file, default_flow_style=False)

# End
