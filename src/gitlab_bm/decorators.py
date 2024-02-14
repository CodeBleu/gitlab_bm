#!/usr/bin/env python
"""
Decorators
"""
import sys
import logging
from .slack import send_to_slack
from .config import config

def notify(func):
    """
    Notify decorator to send message to Slack
    """
    slack_token = config.get_active_config()['slack_token']
    slack_channel_id = config.get_active_config()['slack_channel_id']
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as error:
            notifications_enabled = config.get_active_config().get('notifications_enabled', 'false')
            if notifications_enabled == 'true':
                logging.error(error)
                send_to_slack(slack_token, slack_channel_id, error)
                sys.exit(1)
            else:
                logging.error(error)
                sys.exit(1)

    return wrapper
