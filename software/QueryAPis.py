import tweepy
from tweepy import TweepError

from DB import db
from DataAccess import api
from CustomListener import MyStreamListener


class QueryApi:
    # Dineis posa tweets theleis apo to timeline kai ta vazei direct sth vash
    def getHomeTimeline(self, numOfTweets):
        count = 0
        try:
            for tweet in tweepy.Cursor(api.home_timeline).items(numOfTweets):
                db.insertOne(tweet._json)
                count += 1
                print("\rInserted " + str(count) + " tweets in the db -> ", end="")
        except TweepError as err:  # TODO: na kanei catch kai db errors
            print(err.response)
        raise

    def getStream(self):
        stream = MyStreamListener()
        stream.start()
