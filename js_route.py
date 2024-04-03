#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import subprocess
import os

cwd = os.getcwd()
payload = json.loads(sys.argv[1])
company = payload['view']['state']['values']['ops']['radio_buttons-action']['selected_option']['value']

if company == "nflx":
    subprocess.Popen([f"{cwd}/commands/js_nflx.py", json.dumps(payload)])
elif company == "dis":
    subprocess.Popen([f"{cwd}/commands/js_dis.py", json.dumps(payload)])
elif company == "amzn":
    pass