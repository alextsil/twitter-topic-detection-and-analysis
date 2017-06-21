import pymongo
import csv
from pymongo import MongoClient
from pprint import pprint


client = MongoClient()

db = client['twitter']

tweets = db.tweets
print (db.tweets.count())

all_tweets = tweets.find()


keywords = ['#parisagreement','#climatechange','#parisaccord','#actonclimate','#parisclimatedeal','#climate','#parisclimateaccord','#parisclimateagreement'
            ,'#parisagreeement','#climatechangeisreal']
counter = 0
for tweet in all_tweets:
    filename = '%d.txt' %counter
    file = open(filename,'w')
    if any(keyword in tweet['text'].lower() for keyword in keywords):
        if not tweet['text'].startswith("RT"):
         file.write(tweet['text'])
         counter+=1
         print (tweet['text'])
print ('files created')








