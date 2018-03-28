import tweepy
from tweepy import OAuthHandler


consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

api.retry_count = 5
api.retry_delay = 5
api.timeout = 10
api.wait_on_rate_limit = True
api.wait_on_rate_limit_notify = True
