# -*- coding: utf-8 -*-

import os
try:
    import yaml
except ImportError:
    pass
import sys
from toolz import merge


# ref: https://github.com/spotify/postgresql-metrics/blob/master/postgresql_metrics/common.py
# ref: https://github.com/henriquebastos/python-decouple/blob/master/decouple.py

def _caller_path():
    # MAGIC! Get the caller's module path.
    frame = sys._getframe()
    path = os.path.dirname(frame.f_back.f_back.f_code.co_filename)
    return path


def find_file(target_file, search_path=None):
    search_path = os.path.split(os.path.abspath(target_file))[0] if search_path is None else search_path
    # look for all files in the current path
    filename = os.path.join(search_path, target_file)
    if os.path.isfile(filename):
        return filename

    # search the parent
    parent = os.path.dirname(search_path)
    if parent and parent != os.path.sep and os.path.split(parent)[-1] != '':
        return find_file(target_file, parent)

    # reached root without finding any files.
    return ''


def merge_configs(to_be_merged, default):
    """Merges two configuration dictionaries by overwriting values with
    same keys, with the priority on values given on the 'left' side, so
    the to_be_merged dict.
    Notice that with lists in the configuration, it skips from the default
    (right side) the tuples in that which already exist in the left side
    to_be_merged list. This is used to be able to override time intervals for
    default values in the configuration.
    Example:
    In [1]: x = [["get_stats_disk_usage_for_database", 180],
                 ["get_stats_tx_rate_for_database", 500]]
    In [2]: y = [["get_stats_seconds_since_last_vacuum_per_table", 60],
                 ["get_stats_tx_rate_for_database", 60]]
    In [3]: merge_configs(x, y)
    Out[3]:
    [['get_stats_disk_usage_for_database', 180],
     ['get_stats_tx_rate_for_database', 500],
     ['get_stats_seconds_since_last_vacuum_per_table', 60]]
    """
    if isinstance(to_be_merged, dict) and isinstance(default, dict):
        for k, v in default.items():
            if k not in to_be_merged:
                to_be_merged[k] = v
            else:
                to_be_merged[k] = merge_configs(to_be_merged[k], v)
    elif isinstance(to_be_merged, list) and isinstance(default, list):
        same_keys = set()
        for x in to_be_merged:
            for y in default:
                if isinstance(x, (list, set, tuple)) and isinstance(y, (list, set, tuple)) and len(
                        x) > 0 and len(y) > 0 and x[0] == y[0]:
                    same_keys.add(x[0])
        for y in default:
            if not isinstance(y, (list, set, tuple)) or y[0] not in same_keys:
                to_be_merged.append(y)
    return to_be_merged


def find_and_parse_config(config, default_config='default.yaml'):
    """Finds the service configuration file and parses it.
    Checks also a directory called default, to check for default configuration values,
    that will be overwritten by the actual configuration found on given path.
    """

    def load_config(path):
        if os.path.isfile(path):
            with open(path, 'r') as f:
                config_dict_ = yaml.load(f)
            return config_dict_

    config_path = find_file(config)
    default_path = find_file(default_config)
    config = load_config(config_path)
    default_config = load_config(default_path)
    if config is None and default_config is None:
        raise ValueError('Both config and default_config return None')
    if config is None:
        config_dict = default_config
    elif default_config is None:
        config_dict = config
    else:
        config_dict = merge(default_config, config)

    return config_dict


def add_parent_path(name, level):
    current_path = os.path.abspath(name)
    sys.path.append(os.path.sep.join(current_path.split(os.path.sep)[:-level]))
