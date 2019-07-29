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

class Parse:
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
            pprint.pprint(tweets)

            # Store the url and tweet in a dictionary as a key value pair
            if rt == 'n':
                tweet_list = [{"https://twitter.com/" + t.user.screen_name + "/status/" + str(t.id): (t.text, t.entities.media_url_https)} for t in tweets if re.search('RT', t.text) == None]
            else:
                tweet_list = [{"https://twitter.com/" + t.user.screen_name + "/status/" + str(t.id): (t.text, t.entities.media_url_https)} for t in tweets]
            for t in tweet_list:
                statuses.update(t)

        return statuses

    def search_tweets(tweet_dict, flags):

        flagged_dict = dict()

        # Get every tweet from the dictionary and search for
        # matches in the flags list
        for u, t in tweet_dict.items():
            for f in flags:
                if not re.search(f, t) == None:
                    print("Found the word {} in \"{}\".".format(f, t))
                    flagged_dict.update({u: t})

        return flagged_dict
