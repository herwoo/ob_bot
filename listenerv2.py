#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
import subprocess
import json

# Initialize SocketModeClient with an app-level token + WebClient
client = SocketModeClient(
    # This app-level token will be used only for establishing a connection
    app_token=os.environ.get("OB_APP_TOKEN"),  # xapp-A111-222-xyz
    # You will be using this WebClient for performing Web API calls in listeners
    web_client=WebClient(token=os.environ.get("OB_BOT_TOKEN"))  # xoxb-111-222-xyz
)

from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

cwd = os.getcwd()

def process(client: SocketModeClient, req: SocketModeRequest):
    payload = req.payload
    # Acknowledge all request
    response = SocketModeResponse(envelope_id=req.envelope_id)
    client.send_socket_mode_response(response)
    subprocess.Popen([f"{cwd}/cnc.py", json.dumps(req.payload), req.type])

# Add a new listener to receive messages from Slack
# You can add more listeners like this
client.socket_mode_request_listeners.append(process)
# Establish a WebSocket connection to the Socket Mode servers
client.connect()
# Just not to stop this process
from threading import Event
Event().wait()
