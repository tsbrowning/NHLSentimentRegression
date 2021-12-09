#!/usr/bin/env python3

import argparse
import json
import snscrape.modules.twitter
import sys

parser = argparse.ArgumentParser(description = 'Player Handle')
parser.add_argument('--handle', dest='handle', type=str, help="Player's Twitter handle")
arg = parser.parse_args()

handle = str(sys.argv[2])

query = 'from:' + handle + ' since:2005-01-01'
out_file = handle + '.txt'

scraper = snscrape.modules.twitter.TwitterSearchScraper(query)
with open(out_file, 'w', encoding = 'utf-8') as e:
    e.write(query)
    for tweet in scraper.get_items():
        tweet = str(tweet.json())
        json_object = json.loads(tweet)
        line = []
        c = str(json_object['content'])
        d = str(json_object['date'])
        line.append(c)
        line.append(d)
        l = ' * '.join(line)
        e.write(l)
        e.write('\n')