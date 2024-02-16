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

    def load_config_file(self):
        """
        Load config file
        """
        file_config = {}
        for config_location in CONFIG_LOCATIONS:
            if os.path.isfile(config_location):
                logging.debug("Config file found at %s", config_location)
                with open(config_location, 'r', encoding="utf-8") as file:
                    try:
                        file_config = yaml.safe_load(file)
                        break
                    except yaml.parser.ParserError:
                        msg = f"Config file {config_location} is not valid YAML"
                        logging.error(msg)
                        os._exit(1)

        return file_config

    def get_os_env(self):
        """
        Parse OS environment variables
        """
        glbm_os_env = {k[5:].lower(): v for k, v in os.environ.items() if k.startswith("GLBM_")}

        if 'skip_backup_options' in glbm_os_env:
            try:
                glbm_os_env['skip_backup_options'] = json.loads(glbm_os_env['skip_backup_options'])
            except json.JSONDecodeError:
                bad_value = glbm_os_env.pop('skip_backup_options', None)
                msg = f"OS Env. Variable 'skip_backup_options' is not a list: {bad_value}"
                logging.error(msg)
                if ('notifications_enabled' in glbm_os_env
                    and 'slack_token' in glbm_os_env
                    and 'slack_channel_id' in glbm_os_env
                    and glbm_os_env['notifications_enabled'].lower() == 'true'):
                    send_to_slack(glbm_os_env['slack_token'], glbm_os_env['slack_channel_id'], msg)
                    os._exit(1)
                else:
                    logging.error("Missing Slack Token and/or Slack Channel ID")
                    os._exit(1)

        return glbm_os_env

    def get_active_config(self):
        """
        Get combined config settings
        Furthest to the right in exmaple below wins!
        The order of use is: os_env -> file ('/etc/glbm_config.yaml' OR ~/.config/glbm/config.yaml )
        """
        return self.get_os_env() | self.load_config_file()

config = Config()
