#!/usr/bin/env python3

from parse_class import Parse
import pprint

parse = Parse(new_username='kyleedwards_27', new_rt=True, new_choice=1, new_shorten=False)

print(type(parse))

print(parse.username)
print(parse.rt)
print(parse.choice)
print(parse.shorten)


for i in parse.get_tweets():
    pprint.pprint(i)
