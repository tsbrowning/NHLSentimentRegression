#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 04:30:00 2021

@author: travis


"""


import argparse
import csv
from bs4 import BeautifulSoup
from dateutil.parser import parse
import os
import pandas as pd
import pytz
import re
import requests
import sys
import time

game_logs = []
years = []
games_played = []


def in_dst(date):
    #Example datetime range to be expanded for all years from 2015
    #Currently using DST dates in 2017
    #Example player (Garrett Sparks) didn't play in 2017, subbing in 2016
    DST = pd.date_range(start ='2016-03-12 02:00:00', end='2016-11-05 02:00:00', freq='30min' ).to_list()
    if date in DST:
        print(f'GAME IN DST: {date}')
    else:
        print(f'OUTSIDE OF DST: {date}')


def find_year(profile):
    print('searching for seasons')
    player = requests.get(profile)
    soup = BeautifulSoup(player.text, 'lxml')
    ##Games from the 12-13 season onwards are listed with gametime on hockey-reference
    ##This can be used to better label tweets as pregame and postgame in the SQL section
    ##Perhaps this will be more effectively addressed in the sql section >:/
    for a in soup.find_all('a', href=True):
        addy = a['href']
        addy = f'https://www.hockey-reference.com{addy}'
        if re.search('gamelog/\d{4}', addy):
            if addy in game_logs:
                continue
            else:
                
                game_logs.append(addy)
                years.append(addy[-4:])
                

    print(years)
    print(f'{len(game_logs)} seasons found')

def scrape_stats (player_url):    
    start = time.perf_counter()

    with open(out_file, 'w', encoding = 'utf-8', newline = '\n') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        find_year(player_url)
        headers = ['puckdrop', 'decision', 'goals against', 'shots against', 'saves',\
                   'save %']
        writer.writerow(headers)
        for yr, log in zip(years, game_logs):
            lap = time.perf_counter()
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
                            puckdrops = row.find_all(href=True)
                            for date in puckdrops:
                                box_score = date['href']
                                
                                if box_score.startswith('/box'):

                                    ##Scrape puckdrop time from here using requests and bs4
                                    ##Attach to date in a datetime format
                                    bs = f'https://www.hockey-reference.com{box_score}'
                                    bs = requests.get(bs)
                                    bs = BeautifulSoup(bs.text, 'lxml')
                                    box_score = bs.find('div', {'class' : 'scorebox_meta'})
                                    d1 = box_score.find('div')
                                    d1 = str(d1)
                                    puckdrop = re.search('(?<=\d{4}, ).*(?= PM\<\/div)', d1).group()
                                    #regx to locate hour in 08:00 format <.*(?=:)>
                                    
                                    
                                    
                            #This works for EST games, which is most NHL Arenas, but not all of them.
                            #Next up is a function that assigns a timezone, 
                            #based off of the location in the boxscore scraped above.
                            test = f'{col} {puckdrop}'
                            d = parse(test)
                            in_dst(d)
                            
                            col = f'{col} {puckdrop}-5:00'
                            dt = parse(col)
                            
                            localtime = dt.astimezone(pytz.timezone('US/Eastern'))
                            out.append(localtime)
                            yr = col[:4]
                        
                    elif count == 7:
                        out.append(col)
                    elif count == 8:
                        out.append(col)
                    elif count == 9:
                        out.append(col)
                    elif count == 10:
                        out.append(col)
                    elif count == 11:
                        out.append(col)

                if out:
                    writer.writerow(out)
            
            end = time.perf_counter()
            runtime = end-lap
            print(f'''summary of {yr} season: 
            {len(rows)} games scraped in {runtime} seconds''')
            
    print(f'{len(game_logs)} seasons scraped in {end-start} seconds')

    
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
    for gm in game_logs:
        scrape_stats(gm)