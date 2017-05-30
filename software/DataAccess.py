import tweepy
from tweepy import OAuthHandler


consumer_key = 'hmf5KNglLMA27Ada5lHiNPtLP'
consumer_secret = 'zUDjDmlbIoDKOqPLRBtcyru5ShO35UQ8C9ckzvHGZLAqj2SloU'
access_token = '849017973880877056-RzWXZlwBKxikZCRFnIrSzl0zjtqUHFp'
access_secret = 'w5FpLEwge3n6kgkHkOtrxK8PYFYLrCCsLNULwVmDYkR0f'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

api.retry_count = 5
api.retry_delay = 5
api.timeout = 10
api.wait_on_rate_limit = True
api.wait_on_rate_limit_notify = True
