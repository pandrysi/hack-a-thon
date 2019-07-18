#!/usr/bin/env python3

import os
import sys
import pprint
import requests
import json
import re
import cgitb
import tweepy
import itertools
import random
import markovify
import sys
import time

swear = ['fuck','shit','bitch','dick','drunk','af',]
slang = ['i can\'t even', 'lit', 'turnt', 'chill', 'gucci']
alc = ['vodka', 'tequila', 'rum', 'jager', 'sake', 'beer', 'natty', 'whiteclaw']

def auth_twitter(key="XXiOOh6ikh26NpVaVhNnVMXlF", sec_key="TigPzzltfJVMbuyjKgI1mwaaASoiTK9jD7IpCOXE8jPkNnj2YM", token="724802479-Qt76oHn3clpt72jZiQs7OL5N7dGLqcgUDN5s2O1q", sec_tok="2F6gAUeYbNzOGSCIGEjIL27rbEtFjNXQada4d98THpASb"):
    auth = tweepy.OAuthHandler(key, sec_key)
    auth.set_access_token(token, sec_tok)

    # Get API access
    api = tweepy.API(auth)
    # Verify and return api or Exit
    try:
        api.verify_credentials()
        #print("Authentication OK")
        return api
    except:
        print("Error during Authentication")
        sys.exit()

def get_tweets(username, api, pages):

    tweet_dict = dict()

    tweet = (api.user_timeline(screen_name=username, page = i) for i in range(pages))

    for t in tweet:
        tweet_dict.update(t)

    return tweet_dict
        '''
        tweets_for_csv = [filter_status(tweet.text) for tweet in tweets]

        for j in tweets_for_csv:
            status.append(j)
        '''
    #pprint.pprint(status)
    #return status

def search_tweets(tweet_dict, flags):

    flagged_dict = dict()

    # Get every tweet from the dictionary and search for
    # matches in the flags list
    for t in tweet_dict:
        text = t.text()
        for f in flags:
            if not re.search(f, t) == None:
                flagged_dict.update(t)

    return flagged_dict

if __name__ = '__main__':

    tweet_dict = dict()
    pages = 500

    # Authenticate and return the API
    api = auth_twitter()

    # Get parsing data from user
    user = input("Who is the user you would like to search? ")
    pages = input("How many pages would you like to search? (Default is 500)")

    # Add tweets to tweet_dict
    tweet_dict = get_tweets(user, api, pages)

    print("What key words would you like to search your tweets for?\n\t1. Swear words\n\t2. Slang\n\t3. Alcohol/Drug References\n\t4. All of the above (Default)\n")
    choice = input("Enter selection: ")

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


    '''
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
    '''
