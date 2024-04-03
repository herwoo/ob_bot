#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from slack_sdk.web import WebClient
import requests
import sys
import json

client = WebClient(token=os.environ.get("OB_BOT_TOKEN"))

try:
        payload = json.loads(sys.argv[1])
        channel_id = payload['event']['channel']
        message_ts = payload['event']['ts']

        my_json = requests.get('https://api.beta.swaggystocks.com/wsb/sentiment/rating?timeframe=12+hours')
        my_data = my_json.json()
        xxx = [(x['ticker'],x['total'],x['positive'],x['negative']) for x in my_data][:15]

        msg = "*These are the 15 most mentioned tickers in WallStreetBet Reddit past 12 hours:*\n"+"\n".join([f">*{x[0]}*: Total: {x[1]}, Positive: {x[2]}, Negative: {x[3]}" for x in xxx])
        client.chat_postMessage(
                channel=channel_id,
                thread_ts=message_ts,
                text=msg)

        sys.exit()

except Exception as e:
        print(e)