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

'''
if __name__=='__main__':

    tweet_dict = dict()
    pages = 10
    user = 'demotoss'

    # Authenticate and return the API
    api = auth_twitter()

    # Get parsing data from user
    user = input("Who is the user you would like to search? ")
    pages = input("How many pages would you like to search? (Default is 500)")
    pages = int(pages)
    rt = input("Would you like to see retweets as well? (y/n)")

    # Add tweets to tweet_dict
    tweet_dict = get_tweets(user, api, pages, rt)

    print("What key words would you like to search your tweets for?\n\t1. Swear words\n\t2. Slang\n\t3. Alcohol/Drug References\n\t4. All of the above (Default)\n")
    choice = input("Enter selection: ")
    choice = int(choice)

    flagged = dict()
    all = swear + slang + alc

    if choice == 1:
        flagged = search_tweets(tweet_dict, swear)
    elif choice == 2:
        flagged = search_tweets(tweet_dict, slang)
    elif choice == 3:
        flagged = search_tweets(tweet_dict, alc)
    else:
        flagged = search_tweets(tweet_dict, all)

    pprint.pprint(flagged)
'''
