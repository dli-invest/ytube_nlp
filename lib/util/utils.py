import yaml
import os
from distutils.dir_util import copy_tree


def get_config(upload_file="config.yml"):
    exists = os.path.isfile("stocks/config.yml")
    if exists:
        config_file = "stocks/config.yml"
        # Store configuration file values
    else:
        # Keep presets
        config_file = upload_file
    with open(config_file, "r") as ymlfile:
        # Latest version
        if hasattr(yaml, "FullLoader"):
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        # PyYaml 3.
        else:
            cfg = yaml.load(ymlfile)
    return cfg


def copy_files(fromDirectory, toDirectory):
    copy_tree("/a/b/c", "/x/y/z")