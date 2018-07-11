"""
A script that identified bots mf
"""
# coding: utf-8
# !/usr/bin/python3
# Author: James Campbell
# License: Please see the license file in this repo
# First Create Date: 28-June-2018
# Requirements: minimal. check requirements.txt and run pip/pip3 install -f requirements.txt

# imports section
import base64
import requests
import argparse
import markovify
from pprint import pprint
from statistics import mean
import markovgen
import pandas as pd
from twitter_scraper import get_tweets
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from bs4 import BeautifulSoup
import datetime

# globals
__version__ = "0.1.0"
logo = """                                                                                                                          
  TAYNE TAYNE TAYNE TTTTT AAAA YYY NN EE                                                     
 ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   
                                                    │  
 │                                   *****          ███
                                 *****   *****      │██
 │  ■■■■■■■      ■  ■         ***            ***    ███
       ■ ■    ■  ■ ■  ■■■■    *         *****  **   │██
 │     ■ ■ ■■■■ ■■■■  ■         ***** *******       ███
       ■ ■■  ■■ ■ ■■  ■■■■■     *****  ****** *     │██
 │     ■  ■ ■■  ■  ■  ■         *****         *     ███
            ■   ■     ■■■■           ****    **     │██
 │                             **    *****   *      ███
                                **  ******   *      │██
 │                                **        **      ███
                                   **      **       │██
 │                                   *******        ███
                                                    │██
 └ ─█─█─█─█─█─█─█─█─█─█─█─█─█─█─█─█─█─█─█─█─█─█─█─█─███
   ████████████████████████████████████████████████████
   ████████████████████████████████████████████████████
""" 
itunes_url_endpoint = 'https://itunes.apple.com/search?term={}&country=us&entity={}'
that_url='aHR0cHM6Ly9tb2JpbGUudHdpdHRlci5jb20='
# arguments
parser = argparse.ArgumentParser(description='collects and processes itunes data including ibook, application, and other store items with metadata, run "python3 test_itunize.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-u', '--username', help='username to search', default='jamescampbell', required=False)
parser.add_argument('-n', '--no-logo', dest='logo_off', help='disables printing logo', action='store_true', default=False)
parser.add_argument('-t', '--test', help='prints out james campbell data', action='store_true', default=False)
parser.add_argument('-v', '--verbose', help='print more stuff', action='store_true')
args = parser.parse_args()


# functions section


def get_content(username):
    """Get data."""
    if username:
        tweets = [t for t in get_tweets(username, pages=25)]
    else:
        tweets = ['error', 'no username set properly']
    return tweets


def get_mean(jsondata):
    """Get average of list of items using numpy."""
    if len(jsondata['results']) > 1:
        return mean([float(price.get('price')) for price in jsondata['results'] if 'price' in price])  # key name from itunes
        # [a.get('a') for a in alist if 'a' in a]
    else:
        return float(jsondata['results'][0]['price'])

def get_other_mean(data):
    if len(data) > 1:
        return mean(data)

# main section


def main():
    """Main function that runs everything."""
    if not args.logo_off:  # print or not print logo
        print(logo)
    if args.test:
        #r = requests.get(base64.b64decode(that_url).decode('utf8')+'/jamescampbell')
        tweets = '\n'.join([t['text'] for t in get_tweets('jamescampbell', pages=20)])
        if args.verbose:
            text_model = markovify.Text(tweets)
            print(text_model.make_short_sentence(140))
            exit()
            #print(r.text)
        exit()
    else:
        tweets = get_content(args.username)
        if args.verbose:
            tweetbreak = []
            print(f"Total found: {len(tweets)}")
            print(f"First tweet {tweets[0]['time']}")
            for idx, tweet in enumerate(tweets):
                timeone = tweet['time']
                try:
                    timetwo = (tweets[idx+1]['time'])
                except:
                    timetwo = tweet['time']
                #print(timetwo)
                tdelta = timeone - timetwo
                #print(tdelta.total_seconds())
                tweetbreak.append(tdelta.total_seconds())
            # print(tweetbreak[0])
            print("Average time between tweets: {} minutes".format(get_other_mean(tweetbreak)/60))
            exit()
    jsondata = request_response.json()
    # [trend['name'] for trend in the_data[0]['trends']]
    print()
    if args.print_me:  # if we are running a test or not
        print('json data:')
        pprint(jsondata)
        print('fields available:')
        for k,v in jsondata['results'][0].items():
            print(k)
        exit('thanks for trying')
    average_price = get_mean(jsondata)
    print("The average price of the \033[94m{0}\033[0m items matching search term\033[92m {1}\033[0m: ${2:.2f}".format(jsondata['resultCount'], args['search_term'], average_price))
    if args.output_table:  # if we want to output a table instead of json
        print(pd.DataFrame(jsondata['results'], columns=["price", "artistName", "trackName"]))
    else:
        with open('{}.json'.format(args['search_term']), 'w') as f:
            f.write(''.join(str(x) for x in [request_response.json()]))
        exit('file saved as {}.json'.format(args['search_term']))

if __name__ == "__main__":
    main()