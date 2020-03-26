import tweepy
import logging
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Twitter Bot Account
CONSUMER_KEY = 'fOhcPATqGscwQCP5EwgYMtBaL'
CONSUMER_SECRET = 'wfxfy5bcohKmxDKSuopgkvBkG1TYPzljkQwCiY0CirIjp0IgMG'
ACCESS_KEY = '1241609485929635841-ucvgp499YYtZkxwKD5XyB3P6iNf8ml'
ACCESS_SECRET = 'UQa7RzbcpdkziD8WjdPqYSyqW0fctuDjAMEPBUywiCois'
CALLBACK_URL = 'https://rizahassan.dev/listener'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# api.update_status(
#     status="Hi!👋🏽 I am @YourCoronaBot. \n\nI am here to provide you with the latest information of Covid-19 cases around the globe. \n\nTo start, tweet '@YourCoronaBot coronavirus (name of country)'", auto_populate_reply_metadata=True)

api.update_status(
    status="Hi!👋🏽 I am @YourCoronaBot. \n\n I am back and I apologize for not replying to your tweets. \n\nI was fortunate because it was only some bugs and not viruses\n\nMore data will be added soon!", auto_populate_reply_metadata=True)
