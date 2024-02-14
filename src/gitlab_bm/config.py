#!/usr/bin/env python
"""
GLBM Config Module
"""

import os
import json
import logging
from pathlib import Path
import yaml
from .slack import send_to_slack

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

    def load_config_file(self):
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
                            msg = f"Config file {config_location} is not valid YAML"
                            logging.error(msg)
                            os._exit(1)
            else:
                logging.info("No Config file found - Using OS Env. Variables")

        return self.loaded_config

    def get_os_env(self):
        glbm_os_env = {k[5:].lower(): v for k, v in os.environ.items() if k.startswith("GLBM_")}
        if 'skip_backup_options' in glbm_os_env:
            try:
                glbm_os_env['skip_backup_options'] = json.loads(glbm_os_env['skip_backup_options'])
            except json.JSONDecodeError as e:
                bad_value = glbm_os_env.pop('skip_backup_options', None)
                glbm_os_env.update(self.loaded_config)
                msg = "OS Env. Variable 'skip_backup_options' is not a list"
                logging.error(msg)
                logging.info("Message sent to channel %s : %s: %s",
                             glbm_os_env['slack_channel_id'], os.uname().nodename, msg)
                print(bad_value)
                if glbm_os_env['notifications_enabled'] == 'true':
                    send_to_slack(glbm_os_env['slack_token'], glbm_os_env['slack_channel_id'], msg)
                os._exit(1)

        return glbm_os_env

    def get_active_config(self):
        active_config = self.load_config_file()
        active_config.update(self.get_os_env())
        return active_config

config = Config()
