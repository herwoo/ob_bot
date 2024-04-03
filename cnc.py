#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import json
import sys

cwd = os.getcwd()
payload = json.loads(sys.argv[1])
my_type = sys.argv[2]

if my_type == "events_api":
    # App mention
    if payload['event']['type'] == "app_mention":
        if payload['event']['text'].replace('<@U06PSFTNNAE>','').strip().lower() == "wsb":
            subprocess.Popen([f"{cwd}/commands/wsb.py", json.dumps(payload)])
        elif payload['event']['text'].replace('<@U06PSFTNNAE>','').strip().lower() == "jackpot":
            subprocess.Popen([f"{cwd}/commands/lotto2.py", json.dumps(payload)])
        elif payload['event']['text'].replace('<@U06PSFTNNAE>','').strip().lower().startswith("tickers"):
            subprocess.Popen([f"{cwd}/commands/ticker.py", json.dumps(payload)])
        elif payload['event']['text'].replace('<@U06PSFTNNAE>','').strip().lower() == "help":
            subprocess.Popen([f"{cwd}/commands/help.py", json.dumps(payload)])
    # Message
    if payload["event"]["type"] == "message":
        pass

elif my_type == "slash_commands":
    if payload['command'] == "/job_search":
        subprocess.Popen([f"{cwd}/commands/js_main.py", json.dumps(payload)])

elif my_type == "interactive":
    if payload.get("type") == "view_submission":
        if payload["view"]["callback_id"] == "js_main":
            subprocess.Popen([f"{cwd}/js_route.py", json.dumps(payload)])