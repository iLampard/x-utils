# -*- coding: utf-8 -*-

import os
import yaml


# ref : https://github.com/spotify/postgresql-metrics/blob/master/postgresql_metrics/common.py


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
        for k, v in default.iteritems():
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


def find_and_parse_config(config_path):
    """Finds the service configuration file and parses it.
    Checks also a directory called default, to check for default configuration values,
    that will be overwritten by the actual configuration found on given path.
    """
    config_filename = os.path.basename(config_path)
    config_root = os.path.dirname(config_path)
    default_root = os.path.join(config_root, 'default')
    config_dict = {}
    for config_dir in (default_root, config_root):
        current_path = os.path.join(config_dir, config_filename)
        if os.path.isfile(current_path):
            with file(current_path, 'r') as f:
                read_config_dict = yaml.load(f)
            config_dict = merge_configs(read_config_dict, config_dict)
    return config_dict
