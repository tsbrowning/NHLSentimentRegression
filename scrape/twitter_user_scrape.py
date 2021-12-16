#!/usr/bin/env python3

import argparse
import json
import os
import snscrape.modules.twitter
import sys
import time

def scrape_tweets (f):    
    counter = 0
    start = time.perf_counter()    
    with open(f, 'w', encoding = 'utf-8') as e:
        for tweet in scraper.get_items():
            counter += 1
            tweet = str(tweet.json())
            json_object = json.loads(tweet)
            line = []
            user = json_object['user']
            c = str(json_object['content'])
            d = str(json_object['date'])
            line.append(d)
            line.append(user.get('displayname'))
            line.append(c)
            l = '\t'.join(line)

            e.write(f'{l}\n')
    end = time.perf_counter()
    runtime = end-start
    print(f'{counter} tweets scraped in {runtime} seconds')

parser = argparse.ArgumentParser(description = 'Player Handle')
parser.add_argument('--handle', dest='handle', type=str, help="Player's Twitter handle")
arg = parser.parse_args()

handle = str(sys.argv[2])

directory = 'data/'

parent_dir = '../'

path = os.path.join(parent_dir, directory)



#query = 'from:' + handle + ' since:2005-01-01'
query = f'from:{handle} since:2005-01-01'
out_file = f'{path}{handle}.txt'
#out_file = path + handle + '.txt'

scraper = snscrape.modules.twitter.TwitterSearchScraper(query)

if os.path.exists(path):
    print(f'Scraping tweet history from {handle}')
    scrape_tweets(out_file)
else:
    print('Creating data directory')
    print(f'Scraping tweet history from {handle}')
    os.mkdir(path)
    scrape_tweets(out_file)