#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from slack_sdk.web import WebClient
import json
import sys
import requests

client = WebClient(token=os.environ.get("OB_BOT_TOKEN"))

payload = json.loads(sys.argv[1])
true = True
false = False

channel_id = payload['view']['private_metadata']
user_id = payload['user']['id']
query = payload['view']['state']['values']['kw']['plain_text_input-action']['value']

postings = []

url = f"https://jobs.netflix.com/api/search?q={query}"
r = requests.get(url)
result = r.json()['records']['postings']
postings = result

page = 2
while len(result) == 20:
    url = f"https://jobs.netflix.com/api/search?q={query}&page={page}"
    r = requests.get(url)
    result = r.json()['records']['postings']
    postings = postings+result
    page += 1

titles = [[x['text'],x['location'],x['created_at'],x['external_id']] for x in postings]
titles = sorted(titles, key = lambda x: x[2], reverse = True)

jobs = [titles[i:i+50] for i in range(0,len(titles),50)] #cutting it into 50, slack message amount limitation

for job in jobs:
    output = "\n".join([f"<https://jobs.netflix.com/jobs/{x[3]}|{x[0]}> [{x[1]}] ({x[2]})" for x in job])
    client.chat_postEphemeral(channel=channel_id, user=user_id, text=output)