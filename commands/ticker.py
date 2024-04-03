#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from slack_sdk.web import WebClient
import yfinance as yf
import sys
import json
import re

client = WebClient(token=os.environ.get("OB_BOT_TOKEN"))

payload = json.loads(sys.argv[1])
channel_id = payload['event']['channel']
message_ts = payload['event']['ts']

text = payload['event']['text'].replace('<@U06PSFTNNAE>','').strip().lower().replace("tickers","").strip().upper()
tickers = [x for x in re.findall(r'[A-Z]*', text) if x != ""]

lmsg = []

def tix(ticker):
    try:
        stock = yf.Ticker(ticker)

        info = stock.info
        hist_1d = stock.history(period='1d')
        hist_1y = stock.history(period='1y')
        current_price = hist_1d['Close'][0].round(2)
        low_1y = round(hist_1y['Low'].min(),2)
        low_diff = round(current_price-low_1y,2)
        high_1y = round(hist_1y['High'].max(),2)
        high_diff = round(high_1y-current_price,2)
        PE = round(info.get('forwardPE'),2)
        target_price = round(info.get('targetMedianPrice'),2)
        if target_price >= current_price:
            target_percent = round((target_price-current_price)/current_price*100+100,2)
        else:
            target_percent = round(-1*((current_price-target_price)/current_price*100),2)

        lmsg.append(f"===*{ticker}*===")
        lmsg.append(f"1 Year Low:            ${low_1y:.2f}(${low_diff:.2f})")
        lmsg.append(f"Current Price:        *${current_price:.2f}*")
        lmsg.append(f"1 Year High:           ${high_1y:.2f}(${high_diff:.2f})")
        lmsg.append(f"Target Price(Median):  ${target_price:.2f} ({target_percent}%)")
        lmsg.append(f"P/E Ratio:              {PE:.2f}")
    except:
        lmsg.append(f"===*{ticker}*===")
        lmsg.append(f"Not a valid ticker!")

if tickers:
    for ticker in tickers:
        tix(ticker)

    msg = "\n".join(lmsg)
    client.chat_postMessage(channel=channel_id,thread_ts=message_ts,text=msg)