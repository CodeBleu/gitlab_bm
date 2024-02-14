#!/usr/bin/env python
"""
GLBM Config Module
"""

import os
import logging
from pathlib import Path
import yaml

# Define the locations where the config file might be located
CONFIG_LOCATIONS = [
    './glbm_config.yaml',
    str(Path.home().joinpath('.config/glbm/config.yaml')),
    '/etc/glbm_config.yaml'
]

class Singleton(type):
    """
    Singleton Class
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=Singleton):
    """
    Config Classs to load from file/OS Env.
    """
    def __init__(self):
        self.loaded_config = None

    def load_config(self):
        """
        Load config file
        """
        if self.loaded_config is None:
            for config_location in CONFIG_LOCATIONS:
                if os.path.isfile(config_location):
                    logging.debug("Config file found at %s", config_location)
                    with open(config_location, 'r', encoding="utf-8") as file:
                        try:
                            self.loaded_config = yaml.safe_load(file)
                            break
                        except yaml.parser.ParserError:
                            logging.error("Config file '%s' is not valid YAML", config_location)
                            os._exit(1)
            else:
                logging.info("No Config file found - Using OS Env. Variables")
                self.loaded_config = {}
        return self.loaded_config

    def get_config_value(self, key, default=None):
        """
        Return config value:
        If Config file is found, use that, else use 'GLBM_' prefixed Env. Vars
        """
        cfg = self.load_config()
        cfg_key = key[5:].lower()
        return cfg.get(cfg_key, os.environ.get(key, default))

config = Config()
