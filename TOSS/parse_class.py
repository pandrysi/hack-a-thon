#!/usr/bin/env python3

#------------------------------------------------------------------
# This is a script that takes in the timeline data from a specified
# user and passes it through a filter that searches for certain
# keywords that are deemed innapropriate for online usage.
# Created: 8/6/2019
#------------------------------------------------------------------

# Possible additions:
# Allow for the addition of other words to look for
# Add multiprocessing

import pprint
import json
import re
import cgitb
import tweepy
import itertools
import functools
import multiprocessing
import time
import requests

TIER1 = ['fuck', 'bitch', 'slut', 'whore', 'cunt', 'death']
TIER2 = ['slammer', 'floko', 'four loko', 'asshole', 'cock']
TIER3 = ['shit', 'dick', 'ass', 'vodka', 'rum', 'chill', 'lit', 'gucci']

ALL = TIER1 + TIER2 + TIER3

ISGD_URL = 'http://is.gd/create.php'

name = 'demotoss'
rt = True
shorten = False
choice = 4

class Parse:

    def __init__(self, new_username, new_rt, new_choice, new_shorten):
        self.username = new_username
        self.rt = new_rt
        self.choice = new_choice
        self.shorten = new_shorten

    def get_username(self):
        return self.username

    def get_rt(self):
        return self.rt

    def get_choice(self):
        return self.choice

    def get_shorten(self):
        return self.shorten

    #=======================================
    #
    # Auth_Twitter uses my twitter developer
    # credentials in order to obtain the data
    #
    #=======================================
    def auth_twitter(key="XXiOOh6ikh26NpVaVhNnVMXlF", sec_key="TigPzzltfJVMbuyjKgI1mwaaASoiTK9jD7IpCOXE8jPkNnj2YM", token="724802479-Qt76oHn3clpt72jZiQs7OL5N7dGLqcgUDN5s2O1q", sec_tok="2F6gAUeYbNzOGSCIGEjIL27rbEtFjNXQada4d98THpASb"):
        auth = tweepy.OAuthHandler(key, sec_key)
        auth.set_access_token(token, sec_tok)

        # Get API access
        api = tweepy.API(auth)
        # Verify and return api or Exit
        try:
            api.verify_credentials()
            return api
        except:
            print("Error during Authentication")
            sys.exit()

    #=======================================
    #
    # Get_Tweets goes through the user's tweets
    # obtains them, filters them, then returns them
    #
    #=======================================
    def get_tweets(username, rt, choice, shorten):

        # Generate the API
        api = auth_twitter()

        # Choose the flags based on the user's selection
        if choice == 1:
            flags = TIER1
        elif choice == 2:
            flags = TIER2
        elif choice == 3:
            flags = TIER3
        else:
            flags = ALL

        # Get all the tweets from the user's timeline and pass them through the filter to see if they are allowed
        c = tweepy.Cursor(api.user_timeline, id=username).items()

        while True:
            # Error checking
            try:
                tweet = c.next()
                url = "https://twitter.com/" + tweet.user.screen_name + "/status/" + str(tweet.id)
                # Shorten the URL option
                if shorten:
                    url = shorten_url(url)

                # Make the url and tweet a key value pair
                t = {"https://twitter.com/" + tweet.user.screen_name + "/status/" + str(tweet.id): tweet.text}
                if rt and re.search('RT', tweet.text) == None:
                    found = search_tweets(tweet.text, flags)
                    if found:
                        yield t
                else:
                    found = search_tweets(tweet.text, flags)
                    if found:
                        yield t

            # Handle the error if the rate limit is exceeded
            except tweepy.TweepError:
                time.sleep(60 * 15)
                continue

            # Handle if there are no more tweets
            except StopIteration:
                break


    #=======================================
    #
    # Search_Tweets uses the user decided flags
    # and the tweet data to check to see if each
    # tweet is clean of if it should be deleted
    #
    #=======================================
    def search_tweets(tweet, flags):
        found = False
        # Get every tweet from the dictionary and search for
        # matches in the flags list
        for f in flags:
            if not re.search(f, tweet, re.I) == None:
                print("Found the word {} in \"{}\".".format(f, tweet))
                found = True

        return found

    # Work in progress
    def shorten_url(url):
    	url = requests.get(ISGD_URL, params={'format': 'simple', 'url': url})
    	#url = url['shorturl']
    	return url
