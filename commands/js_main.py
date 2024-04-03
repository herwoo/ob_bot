#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
import json
import sys

# Initialize SocketModeClient with an app-level token + WebClient
client = SocketModeClient(
    # This app-level token will be used only for establishing a connection
    app_token=os.environ.get("OB_APP_TOKEN"),  # xapp-A111-222-xyz
    # You will be using this WebClient for performing Web API calls in listeners
    web_client=WebClient(token=os.environ.get("OB_BOT_TOKEN"))  # xoxb-111-222-xyz
)

from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

payload = json.loads(sys.argv[1])
true = True
false = False

# Open a new modal
client.web_client.views_open(
    trigger_id=payload["trigger_id"],
    view={
    "type": "modal",
    "callback_id": "js_main",
    "private_metadata": payload['channel_id'],
    "title": {
        "type": "plain_text",
        "text": "Let's get a job!",
        "emoji": true
    },
    "submit": {
        "type": "plain_text",
        "text": "Search!",
        "emoji": true
    },
    "close": {
        "type": "plain_text",
        "text": "Cancel",
        "emoji": true
    },
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Select the company to search jobs"
            }
        },
        {
            "type": "input",
            "element": {
                "type": "radio_buttons",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Netflix (live)",
                            "emoji": true
                        },
                        "value": "nflx"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Disney/Hulu (live)",
                            "emoji": true
                        },
                        "value": "dis"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Amazon Prime (coming soon)",
                            "emoji": true
                        },
                        "value": "amzn"
                    }
                ],
                "action_id": "radio_buttons-action"
            },
            "label": {
                "type": "plain_text",
                "text": "Choices",
                "emoji": true
            },
            "block_id":"ops"
        },
        {
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Keyword",
				"emoji": true
			},
            "block_id":"kw"
		}
    ]
}
)