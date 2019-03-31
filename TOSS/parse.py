#!/usr/bin/env python3

import os
import sys
import pprint
import requests
import json
import re
import cgitb

flags = ['fuck','shit','bitch','dick','drunk']

with open("awful_person_demo.json", "r") as read_file:
    data = json.load(read_file)

creation = data['statuses']

print "Content-type: text/html\r\n\r\n";
for item in creation:
    create = item['created_at']
    text = item['text']
    for word in flags:
        if re.search(word, text, re.I):
            print "<p>Date: %s\nTweet:%s<\p>" % (create, text)
            break
