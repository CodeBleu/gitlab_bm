#!/usr/bin/env python
"""
Slack Module
"""

import os
import sys
import html
import re
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_to_slack(slack_token, slack_channel_id, message):
    """
    Send message to slack channel
    """

    hostname = os.uname().nodename

    # Initialize a Web API client
    if (slack_token is not None
            and slack_channel_id is not None):
        client = WebClient(token=slack_token)
    else:
        logging.error("Message not sent to Slack:"
                      " Missing TOKEN or CHANNEL_ID in OS env or config.yaml")
        sys.exit(1)

    # Prepare the message payload
    data = {
        "channel": slack_channel_id,
        "text": f"{hostname}: {message}"
    }

    try:
        # Call the chat.postMessage method using the WebClient
        response = client.chat_postMessage(**data)

        # Check if the message was successfully posted
        html_unescaped = html.unescape(response["message"]["text"])
        clean_message = re.sub('<|>', '', html_unescaped)
        assert clean_message ==  f"{hostname}: {message}"
        logging.info("Message sent to channel %s : %s: %s",
                slack_channel_id, hostname, message)

    except SlackApiError as error:
        # You will get a SlackApiError if "ok" is False
        logging.error("Error posting message: %s",error)
