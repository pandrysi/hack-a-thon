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
# Teach Machine learing a bit more so it works better

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
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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

def get_tweets(username, api, rt, shorten, level):

    # Get all the tweets from the user's timeline and pass them through the filter to see if they are allowed
    c = tweepy.Cursor(api.user_timeline, id=username).items()

    while True:
        # Error checking
        try:
            tweet = c.next()
            url = "https://twitter.com/" + tweet.user.screen_name + "/status/" + str(tweet.id)

            # Shorten the URL option
            if shorten == 'y':
                url = shorten_url(url)

            t = {"https://twitter.com/" + tweet.user.screen_name + "/status/" + str(tweet.id): tweet.text}
            if rt == 'n' and re.search('RT', tweet.text) == None:
                found = search_tweets(tweet.text, level)
                if found:
                    yield t
            else:
                found = search_tweets(tweet.text, level)
                if found:
                    yield t
        except tweepy.TweepError:
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break


def search_tweets(tweet, level):

    found = False

    if level == 1:
        rate = -0.25
    elif level == 2:
        rate = -0.5
    elif level == 3:
        rate = -0.75
    else:
        rate = -0.5

    # Uses machine learning to detect whether or not it is negative
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(tweet)

    # If the negative score outweighs the positive it flags it
    if vs['compound'] < rate:
        print("Tweet: {}\nPos: {}\nNeg: {}\nCompound: {}".format(tweet, vs['pos'], vs['neg'], vs['compound']))
        found = True

    return found

# Work in progress
def shorten_url(url):
	url = requests.get(ISGD_URL, params={'format': 'simple', 'url': url})
	#url = url['shorturl']
	return url

if __name__=='__main__':

    tweet_dict = dict()
    pages = 10
    user = 'demotoss'

    # Authenticate and return the API
    api = auth_twitter()

    # Get parsing data from user
    user = input("Who is the user you would like to search? ")
    rt = input("Would you like to see retweets as well? (y/n)")
    shorten = input("Would you like to shorten the link? (y/n)")
    level = input("What level of filtering would you like to do?\n1. High\n2. Mid\n3. Low\n")
    level = int(level)

    count = 0
    # Return all the tweets
    for i in get_tweets(user, api, rt, shorten, level):
        count += 1
        pprint.pprint(i)

    print('{} tweets flagged.'.format(count))
