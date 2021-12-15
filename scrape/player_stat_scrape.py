#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 04:30:00 2021

@author: travis


"""


import argparse
import csv
from bs4 import BeautifulSoup
import os
from re import search
import requests
import sys
import time

game_logs = []
years = []
games_played = []

def find_year(profile):
    print('searching for seasons')
    player = requests.get(profile)
    soup = BeautifulSoup(player.text, 'lxml')
    for a in soup.find_all('a', href=True):
        addy = a['href']
        addy = f'https://www.hockey-reference.com{addy}'
        if search('gamelog/\d{4}', addy):
            if addy in game_logs:
                continue
            else:
                game_logs.append(addy)
                years.append(addy[-4:])

    print(years)
    print(f'{len(game_logs)} seasons found')

def scrape_stats (player_url):    
    counter = 0
    start = time.perf_counter()

    with open(out_file, 'w', encoding = 'utf-8', newline = '\n') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        find_year(player_url)
        headers = ['date', 'goals', 'assists', '+/-', 'pim',\
                   'shots', 'shot%', 'TOI', 'hits',\
                   'blocks', 'faceoff %']
        writer.writerow(headers)
        for yr, log in zip(years, game_logs):
            year = requests.get(log)
            year = BeautifulSoup(year.text, 'lxml')
            
            table = year.find('tbody')
            rows = table.findChildren(['tr'])

            
            for row in rows:
                cols = row.find_all('td')
                cols = [x.text.strip() for x in cols]
                yr = 0
                out = []
                for count, col in enumerate(cols):
                    if count == 0:
                        if col in games_played:
                            break
                        else:
                            games_played.append(col)
                        
                            out.append(col)
                            yr = col[:4]
                        
                    elif count == 7:
                        out.append(col)
                    elif count == 8:
                        out.append(col)
                    elif count == 10:
                        out.append(col)
                    elif count == 11:
                        out.append(col)
                    elif count == 19:
                        out.append(col)
                    elif count == 20:
                        out.append(col)
                    elif count == 22:
                        out.append(col)
                    elif count == 23:
                        out.append(col)
                    elif count == 24:
                        out.append(col)
                    elif count == 27:
                        out.append(col)

                if out:
                    writer.writerow(out)
            
            end = time.perf_counter()
            runtime = end-start
            print(f'''summary of {yr} season: 
            {len(rows)} games scraped in {runtime} seconds''')        

    
parser = argparse.ArgumentParser(description = 'Player Handle')
parser.add_argument('--player', dest='player', type=str, help="NHL player")
arg = parser.parse_args()

player = str(sys.argv[2])
name = player[2:]

player_url = f'https://www.hockey-reference.com/players/{player}.html'
directory = 'data/'
parent_dir = '../'
path = os.path.join(parent_dir, directory)
out_file = f'{path}{name}_stats.csv'



if os.path.exists(path):
    print(f'Scraping statistical history for {player}')
    #scrape_stats(out_file)
    scrape_stats(player_url)
    
else:
    print('Creating data directory')
    print(f'Scraping statistical history for {player}')
    os.mkdir(path)
    find_year(player_url)
    for gm in gmlogs:
        scrape_stats(gm)