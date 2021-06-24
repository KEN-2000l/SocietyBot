import os
from collections.abc import Mapping

import yaml

from .functions import log


def load_configs(*, global_path='global_configs.yml', guild_dir='configs/'):
    default_config_path = os.path.dirname(os.path.realpath(__file__)) + '/default_global_configs.yml'
    try:
        global_configs = yaml.safe_load(open(default_config_path, encoding='UTF-8'))
    except FileNotFoundError as e:
        log(f'{e} \nCould not find default Global Configuration File.', tag='Error')
        raise
    new_config_path = os.getcwd() + '/' + global_path
    try:
        new_config = yaml.safe_load(open(new_config_path, encoding='UTF-8'))
    except FileNotFoundError:
        log(f'Did not find Global Configuration File at {new_config_path}; using Defaults.', tag='Info')
    else:
        _recursive_merge(global_configs, new_config)

    guild_prefixes, guild_configs = {}, {}
    guild_configs_dir = os.getcwd() + '/' + guild_dir
    for file in os.listdir(guild_configs_dir):
        file_name = os.path.basename(file).rpartition('.')
        if file_name[-1] == 'yml':
            try:
                config_file = yaml.safe_load(open(guild_configs_dir + file))
                if ('bot' in config_file) and ('prefix' in config_file['bot']):
                    guild_id1 = int(file_name[0])
                    guild_id2 = int(config_file['guild']['id'])
                    if guild_id1 != guild_id2:
                        log(f'Mismatched file name ID and Guild ID in file: {file}')
                        raise
                    guild_prefixes[guild_id2] = config_file['bot']['prefix']
                    guild_configs[guild_id2] = config_file
            except UnicodeDecodeError as e:
                log(f'{e} \nError while decoding Guild Configuration File: {file}', tag='Error')
                raise
            except KeyError as e:
                log(f'{e} \nError parsing data from Guild Configuration file: {file}', tag='Error')
                raise

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
