#!/usr/bin/env python3

#------------------------------------------------------------------
# This is a script that takes in the timeline data from a specified
# user and passes it through a filter that searches for certain
# keywords that are deemed innapropriate for online usage.
# Created: 7/22/2019
#------------------------------------------------------------------

# Possible additions:
# Add tiers of filtering (ex. Fuck is high tier and vodka is low tier)
# Allow for the addition of other words to look for

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

swear = ['fuck','shit','bitch','dick','drunk','slut', 'whore', 'asshole', 'ass', 'cunt']
slang = ['i can\'t even', 'lit', 'turnt', 'chill', 'gucci']
alc = ['vodka', 'tequila', 'rum', 'jager', 'sake', 'beer', 'natty', 'whiteclaw', 'slammer', 'four loko', 'floko']

ISGD_URL = 'http://is.gd/create.php'

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

def get_tweets(username, api, rt, choice, shorten):

    tweet_list = []
    statuses = dict()

    if choice == 1:
        flags = swear
    elif choice == 2:
        flags = slang
    elif choice == 3:
        flags = alc
    else:
        flags = swear + slang + alc

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
                found = search_tweets(tweet.text, flags)
                if found:
                    yield t
            else:
                found = search_tweets(tweet.text, flags)
                if found:
                    yield t
        except tweepy.TweepError:
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break


def search_tweets(tweet, flags):

    found = False
    # Get every tweet from the dictionary and search for
    # matches in the flags list
    for f in flags:
        if not re.search(f, tweet, re.I) == None:
            print("Found the word {} in \"{}\".".format(f, tweet))
            found = True

    return found

def shorten_url(url):
	url = requests.get(ISGD_URL, params={'format': 'json', 'url': url})
	url = url.json()
	url = url['shorturl']
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
    shorten = input("Would you like to shorten the URL? (y/n)")

    print("\nWhat key words would you like to search your tweets for?\n\t1. Swear words\n\t2. Slang\n\t3. Alcohol/Drug References\n\t4. All of the above (Default)\n")
    choice = input("Enter selection: ")
    choice = int(choice)

    flagged = dict()
    all = swear + slang + alc

    count = 0
    # Return all the tweets
    for i in get_tweets(user, api, rt, choice, shorten):
        count += 1
        pprint.pprint(i)

    print('{} tweets flagged.'.format(count))
