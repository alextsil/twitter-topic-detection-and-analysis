import tweepy
from tweepy import TweepError

from DB import db
from DataAccess import api

db = db()

db.printAll()
db.deleteAll()

count = 0
try:
    for tweet in tweepy.Cursor(api.home_timeline).items(10000):
        db.insertOne(tweet._json)
        count += 1
        print("\rInserted " + str(count) + " tweets in the db -> ", end="")
except TweepError as err:  # TODO: na kanei catch kai db errors
    print(err.response)
    raise
