#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from app import app
import pprint
import json
import re
import cgitb
import tweepy
import itertools
import parse_class

swear = ['fuck','shit','bitch','dick','drunk']
slang = ['i can\'t even', 'lit', 'turnt', 'chill', 'gucci']
alc = ['vodka', 'tequila', 'rum', 'jager', 'sake', 'beer', 'natty', 'whiteclaw']

@app.route('/')

@app.route('/run_twitter')
def parse():
        pages = 10
        user = 'demotoss'
        api = parse_class.auth_twitter()
        rt = 'y'
        tweet_dict = parse_class.get_tweets(user, api, pages, rt)
        all = swear + slang + alc
        flagged = dict()
        flagged = parse_class.search_tweets(tweet_dict, all)

        return render_template('run_twitter.html',)
