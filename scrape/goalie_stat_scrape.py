#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 04:30:00 2021

@author: travis


"""


import argparse
from bs4 import BeautifulSoup
import csv
import datetime
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
DST = []



#This is messy, terrible, an I imagine I can replace this with less than 5 lines of pandas
#See: https://stackoverflow.com/questions/53292178/looking-for-pandas-datetimeindex-is-dst
#BUT IT WORKS FOR NOW

DST12 = pd.date_range(start ='2012-03-11 02:00:00', end='2012-11-04 02:00:00', freq='30min' ).to_list()
DST13 = pd.date_range(start ='2013-03-10 02:00:00', end='2013-11-03 02:00:00', freq='30min' ).to_list()
DST14 = pd.date_range(start ='2014-03-09 02:00:00', end='2014-11-02 02:00:00', freq='30min' ).to_list()
DST15 = pd.date_range(start ='2015-03-08 02:00:00', end='2015-11-01 02:00:00', freq='30min' ).to_list()
DST16 = pd.date_range(start ='2016-03-13 02:00:00', end='2016-11-06 02:00:00', freq='30min' ).to_list()
DST17 = pd.date_range(start ='2017-03-12 02:00:00', end='2017-11-05 02:00:00', freq='30min' ).to_list()
DST18 = pd.date_range(start ='2018-03-11 02:00:00', end='2018-11-04 02:00:00', freq='30min' ).to_list()
DST19 = pd.date_range(start ='2019-03-10 02:00:00', end='2019-11-03 02:00:00', freq='30min' ).to_list()
DST20 = pd.date_range(start ='2020-03-08 02:00:00', end='2020-11-01 02:00:00', freq='30min' ).to_list()
DST21 = pd.date_range(start ='2021-03-14 02:00:00', end='2021-11-07 02:00:00', freq='30min' ).to_list()
DST22 = pd.date_range(start ='2022-03-13 02:00:00', end='2022-11-06 02:00:00', freq='30min' ).to_list()
    
dst_years = [DST12, DST13, DST14, DST15, DST16, DST17, DST18, DST19, DST20, DST21, DST22]
for year in dst_years:
    for hr in year:
        DST.append(hr)
        
def in_dst(target):    
    if target in DST:
        value = f'{target}-0400'
        #print(f'GAME IN DST: {date}')
        return value
        
    else:
        value = f'{target}-0500'
        #print(f'OUTSIDE OF DST: {date}')
        return value


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
                #Cleanup seasons prior to 2012-13 here
                try:
                    year = int(addy[-4:])
                    if year > 2012:
                        game_logs.append(addy)
                        years.append(addy[-4:])
                except:
                    continue
                

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
                            try:
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
                                    d = in_dst(d)
                                    dt = parse(d)
                            
                                localtime = dt.astimezone(pytz.timezone('US/Eastern'))
                                #Adding 12 hours, because games are listed with 
                                #12 hour times and they aren't played during AM hours
                                localtime = localtime + datetime.timedelta(hours = 12)
                                out.append(localtime)
                                yr = col[:4]
                            except:
                                continue
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