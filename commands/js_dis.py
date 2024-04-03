#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from slack_sdk.web import WebClient
import json
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime

client = WebClient(token=os.environ.get("OB_BOT_TOKEN"))

payload = json.loads(sys.argv[1])
true = True
false = False

channel_id = payload['view']['private_metadata']
user_id = payload['user']['id']
keyword = payload['view']['state']['values']['kw']['plain_text_input-action']['value']

def convert2time(my_date):
    return datetime.strptime(my_date, '%b. %d, %Y')

url = f"https://jobs.disneycareers.com/search-jobs/results?ActiveFacetID=0&CurrentPage=1&RecordsPerPage=1000&Distance=100&RadiusUnitType=0&Keywords=&Location=&ShowRadius=False&IsPagination=False&CustomFacetName=industry&FacetTerm=hulu&FacetType=5&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=5&SortDirection=1&SearchType=7&OrganizationIds=391-28648&RefinedKeywords%5B0%5D={keyword}&PostalCode=&ResultsType=0&fc=&fl=&fcf=&afc=&afl=&afcf="

r = requests.get(url)

result = json.loads(r.content)

html = result['results']

soup = BeautifulSoup(html, "html.parser")

rows = soup.find_all("tr")

data = [[x.text.replace("\n","") for x in row.find_all("td")] for row in rows[1:]]
href = [[[y['href'] for y in x.find_all('a')] for x in row.find_all('td')] for row in rows[1:]]

result = [[x[0][0],x[0][1],x[0][2],x[0][3],f"https://jobs.disneycareers.com{x[1][0][0]}"] for x in list(zip(data,href))]

result = sorted(result, key = lambda x: convert2time(x[1]), reverse = True)

jobs = [result[i:i+50] for i in range(0,len(result),50)] #cutting it into 50, slack message amount limitation

for job in jobs:
    output = "\n".join([f"<{x[4]}|{x[0]}> [{x[3]}] ({x[1]}) - {x[2]}" for x in job])
    client.chat_postEphemeral(channel=channel_id, user=user_id, text=output)