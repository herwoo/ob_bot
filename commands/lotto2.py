#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from slack_sdk.web import WebClient
import requests
import sys
import json
from bs4 import BeautifulSoup
from datetime import datetime

client = WebClient(token=os.environ.get("OB_BOT_TOKEN"))

payload = json.loads(sys.argv[1])
channel_id = payload['event']['channel']
message_ts = payload['event']['ts']

lmsg = []

mega_millions = "https://www.megamillions.com/cmspages/utilservice.asmx/GetLatestDrawData"
r_mega = requests.get(mega_millions)
parsed_mega = BeautifulSoup(r_mega.content, features="xml")
mega_data = json.loads(parsed_mega.text)
mega_jackpot = f"${int(mega_data['Jackpot']['NextPrizePool']/1000000)} Million"
mega_time = mega_data['NextDrawingDate']
mega_dt_obj = datetime.strptime(mega_time, "%Y-%m-%dT%H:%M:%S")
mega_drawing = mega_dt_obj.strftime("%a, %b %d, %Y")
lmsg.append(f"Mega Millions: {mega_jackpot} {mega_drawing}")

powerball = "https://www.powerball.com"
try:
    r_power = requests.get(powerball)
    r_html = r_power.content.decode("utf-8")
    parsed_power = BeautifulSoup(r_html, features='lxml')
    power_draw_result = parsed_power.find("div",{"id":"drawResult"})
    power_jackpot = power_draw_result.find("span", attrs={'class':'game-jackpot-number text-xxxl lh-1 text-center'}).text
    power_next = power_draw_result.find('div', {"id":"next-drawing"})
    power_drawing = power_next.find("h5", attrs={'class':'card-title mx-auto mb-3 lh-1 text-center title-date'}).text
except:
    try:
        r_power = requests.get(powerball)
        r_html = r_power.content.decode("utf-8")
        parsed_power = BeautifulSoup(r_html, features='lxml')
        power_draw_result = parsed_power.find("div",{"id":"drawResult"})
        power_jackpot = power_draw_result.find("span", attrs={'class':'game-jackpot-number text-xxxl lh-1 text-center'}).text
        power_next = power_draw_result.find('div', {"id":"next-drawing"})
        power_drawing = power_next.find("h5", attrs={'class':'card-title mx-auto mb-3 lh-1 text-center title-date'}).text
    except:
        try:
            r_power = requests.get(powerball)
            r_html = r_power.content.decode("utf-8")
            parsed_power = BeautifulSoup(r_html, features='lxml')
            power_draw_result = parsed_power.find("div",{"id":"drawResult"})
            power_jackpot = power_draw_result.find("span", attrs={'class':'game-jackpot-number text-xxxl lh-1 text-center'}).text
            power_next = power_draw_result.find('div', {"id":"next-drawing"})
            power_drawing = power_next.find("h5", attrs={'class':'card-title mx-auto mb-3 lh-1 text-center title-date'}).text
        except:
            power_jackpot = "failed to grab."
            power_drawing = "please retry."

lmsg.append(f"Power Ball: {power_jackpot} {power_drawing}")

msg = "\n".join(lmsg)

client.chat_postMessage(channel=channel_id,thread_ts=message_ts,text=msg)

sys.exit()
