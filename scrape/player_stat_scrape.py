#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 04:30:00 2021

@author: travis

Max Jones
Jakob Chychrun
Anton Blidh
Zemgus Girgensons
Zac Rinaldo
Joel Edmundson
Alex DeBrincat
Ian Cole
Devin Shore
John Klinberg
Danny DeKeyser
Connor McDavid
Frank Vatrano
Adrian Kempe
Alex Galchenyuk
Victor Mete
Matt Duchene
Connor Carrick
Noah Dobson
Christian Wolanin
James van Riemsdyk
Jason Zucker
Logan Couture
David Perron
Kevin Shattenkirk
Rasmus Sandin
Garret Sparks
Robin Lehner
Tj Oshie
Antony Bietto
"""


#This will probably require beautiful soup
import argparse
import csv
from bs4 import BeautifulSoup
#import json
import os
import requests
import sys
import time

def scrape_stats (player):    
    counter = 0
    start = time.perf_counter()    
    with open(player, 'w', encoding = 'utf-8', newline = '\n') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter='\t')
        '''
        for tweet in scraper.get_items():
            counter += 1
            tweet = str(tweet.json())
            json_object = json.loads(tweet)
            line = []
            c = str(json_object['content'])
            d = str(json_object['date'])
            line.append(c)
            line.append(d)
            l = ' * '.join(line)
            e.write(f'{l}\n')
            '''
        csv_writer.write(player)
    end = time.perf_counter()
    runtime = end-start
    print(f'{counter} tweets scraped in {runtime} seconds')

parser = argparse.ArgumentParser(description = 'Player Handle')
parser.add_argument('--player', dest='player', type=str, help="NHL player")
arg = parser.parse_args()

source = requests.get('https://www.hockey-reference.com/players/j/jonesma03/gamelog/2021')
soup = BeautifulSoup(source, 'lxml')

player = str(sys.argv[2])

directory = 'data/'

parent_dir = '../'

path = os.path.join(parent_dir, directory)


#query = f'from:{handle} since:2005-01-01'
out_file = path + player + '.csv'


if os.path.exists(path):
    print(f'Scraping statistical history from {player}')
    scrape_stats(out_file)
else:
    print('Creating data directory')
    print(f'Scraping statistical history from {player}')
    os.mkdir(path)
    scrape_stats(out_file)