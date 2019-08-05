#!/usr/bin/env python3

#------------------------------------------------------------------
# This is a script that takes in the timeline data from a specified
# user and passes it through a filter that searches for certain
# keywords that are deemed innapropriate for online usage.
# Created: 7/22/2019
#------------------------------------------------------------------

# Possible additions:
# OPTIMIZE IT. LESS LISTS AND MORE GENERATORS
# Add tiers of filtering (ex. Fuck is high tier and vodka is low tier)
# Allow for the addition of other words to look for
# Implement full timeline history checking

import pprint
import json
import re
import cgitb
import tweepy
import itertools

swear = ['fuck','shit','bitch','dick','drunk','slut', 'whore', 'asshole', 'ass', 'cunt']
slang = ['i can\'t even', 'lit', 'turnt', 'chill', 'gucci']
alc = ['vodka', 'tequila', 'rum', 'jager', 'sake', 'beer', 'natty', 'whiteclaw', 'slammer', 'four loko', 'floko']

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

def get_tweets(username, api, pages, rt):

    tweet_list = []
    statuses = dict()

    # Get all the tweets from the user's timeline within the page range
    for i in range(pages):
        tweets = api.user_timeline(screen_name=username, page = i)

        # Store the url and tweet in a dictionary as a key value pair
        if rt == 'n':
            tweet_list = [{"https://twitter.com/" + t.user.screen_name + "/status/" + str(t.id): t.text} for t in tweets if re.search('RT', t.text) == None]
        else:
            tweet_list = [{"https://twitter.com/" + t.user.screen_name + "/status/" + str(t.id): t.text} for t in tweets]
        for t in tweet_list:
            statuses.update(t)

    return statuses

def search_tweets(tweet_dict, flags):

    flagged_dict = dict()

    # Get every tweet from the dictionary and search for
    # matches in the flags list
    for u, t in tweet_dict.items():
        for f in flags:
            if not re.search(f, t, re.I) == None:
                print("Found the word {} in \"{}\".".format(f, t))
                flagged_dict.update({u: t})

    return flagged_dict

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
