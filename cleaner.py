# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 18:13:03 2021

@author: valer
"""
import os
import time
import json
import csv
from datetime import datetime
import cProfile
import pstats
import functools
from tqdm import tqdm

class Account:
    def __init__(self,tweet):
        self.creation_date = (datetime.now()-datetime.strptime(tweet['user']['created_at'],"%a %b %d %H:%M:%S +0000 %Y")).total_seconds()
        self.verified = tweet['user']['verified']
        try:
            self.bio_length = len(tweet['user']['description'])
        except:
            self.bio_length = 0
        self.id = tweet['user']['id']
            
        self.tweet_count = 1
        self.follow_count = tweet['user']['friends_count']
        self.followers_count = tweet['user']['followers_count']
        self.tweet_length = len(tweet['text'])
        self.tweet_url = int("http" in tweet['text'])
        self.retweet_by_tweet = int(tweet['retweeted'])
        self.hashtag_by_tweet = int(tweet['text'].count('#'))
        self.favorite_count = tweet['favorite_count']
        self.retweet_count = tweet['retweet_count']
        self.quote_count = tweet['quote_count']
        
    def update(self,tweet):
        self.tweet_count += 1
        self.follow_count += tweet['user']['friends_count']
        self.followers_count += tweet['user']['followers_count']
        self.tweet_length += len(tweet['text'])
        self.retweet_by_tweet += int(tweet['retweeted'])
        self.hashtag_by_tweet += int(tweet['text'].count('#'))
        self.tweet_url += int("http" in tweet['text'])
        self.favorite_count += tweet['favorite_count']
        self.retweet_count += tweet['retweet_count']
        self.quote_count += tweet['quote_count']


    def toCSV(self):
        self.follow_count /= self.tweet_count
        self.followers_count /= self.tweet_count
        self.tweet_length /= self.tweet_count
        self.tweet_url /= self.tweet_count
        self.favorite_count /= self.tweet_count
        self.retweet_count /= self.tweet_count
        self.quote_count /= self.tweet_count
        self.retweet_by_tweet /= self.tweet_count
        self.hashtag_by_tweet /= self.tweet_count
        return list(map(int,[self.id,self.creation_date,self.bio_length,self.verified,
                             self.follow_count,self.followers_count,self.tweet_length,
                             self.tweet_url,self.tweet_count,self.favorite_count,
                             self.retweet_count,self.quote_count,self.hashtag_by_tweet,
                             self.retweet_by_tweet
                             ]))

def main(size=2285,batch=10,start=0):
    start_time = time.time()
    accounts = {}
    tweetcount=0
    for index in tqdm(range(start,size)):
        with open('data/raw/raw{}.json'.format(str(index)),encoding='UTF-8') as file:
            for tweet in (json.loads(line) for line in file):
                tweetcount+=1
                name = tweet['user']['name']
                if name not in accounts:
                    accounts[name] = Account(tweet)
                else:
                    accounts[name].update(tweet)
        if (index+1)%batch==0:
            with open('data/cleaned/clean{}.csv'.format(str(index//batch)),'w',encoding='UTF-8',newline="") as cleanfile:
                writer = csv.writer(cleanfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL).writerow
                for account in accounts.values():
                        writer(account.toCSV())
                        del account
            accounts = {}
    print("--- %s seconds ---" % (time.time() - start_time))

def profiler(func):
    cProfile.run(func,'{}.profile'.format(func))
    stats = pstats.Stats('{}.profile'.format(func))
    stats.strip_dirs().sort_stats('time').print_stats()
    
profiler('main(size=10,batch=1)')

# for file in os.listdir('data/cleaned'):
#     os.remove('data/cleaned/{}'.format(file))

#test VGuich