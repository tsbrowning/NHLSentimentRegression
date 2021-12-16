#!/usr/bin/env python3

import argparse
import csv
import json
import os
import snscrape.modules.twitter
import sys
import time

def scrape_tweets (f):    
    counter = 0
    start = time.perf_counter()    
    with open(f, 'w', encoding = 'utf-8', newline = '\n') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        headers = ['date', 'time', 'display name', 'content']
        writer.writerow(headers)
        for tweet in scraper.get_items():
            counter += 1
            tweet = str(tweet.json())
            json_object = json.loads(tweet)
            line = []
            user = json_object['user']
            content = str(json_object['content'])
            date = str(json_object['date'])
            full_date = date.split('T')
            
            for d in full_date:
                line.append(d)
            line.append(user.get('displayname'))
            line.append(content)
            

            writer.writerow(line)
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




query = f'from:{handle} since:2005-01-01'
out_file = f'{path}{handle}.csv'


scraper = snscrape.modules.twitter.TwitterSearchScraper(query)

if os.path.exists(path):
    print(f'Scraping tweet history from {handle}')
    scrape_tweets(out_file)
else:
    print('Creating data directory')
    print(f'Scraping tweet history from {handle}')
    os.mkdir(path)
    scrape_tweets(out_file)