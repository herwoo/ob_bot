#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from slack_sdk.web import WebClient
import requests
import sys
import json

client = WebClient(token=os.environ.get("OB_BOT_TOKEN"))


payload = json.loads(sys.argv[1])
channel_id = payload['event']['channel']
message_ts = payload['event']['ts']


msg = """@OB-uplynk help - list commands
@OB-uplynk jackpot - list lotto winnings with dates
@OB-uplynk wsb - 15 wsb most talked stocks past 12 hours
@OB-uplynk tickers XXX YYY ZZZ - get ticker info"""

client.chat_postMessage(
        channel=channel_id,
        thread_ts=message_ts,
        text=msg)
