#!/usr/bin/env python3

import os
import sys
import pprint
import requests
import json
import re

flags = ['fuck','shit','bitch','dick','drunk']

with open("awful_person_demo.json", "r") as read_file:
    data = json.load(read_file)

creation = data['statuses']

for item in creation:
    create = item['created_at']
    text = item['text']
    for word in flags:
        if re.search(word, text, re.I):
            print('{} \t{}'.format(create, text))
            break
