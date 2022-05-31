import tweepy
from config import settings

TWITTER_SETTINGS = settings['TWITTER']

CLIENT = tweepy.Client(
    bearer_token=TWITTER_SETTINGS['BEARER_TOKEN'],
    consumer_key=TWITTER_SETTINGS.CLIENT_ID,
    consumer_secret=TWITTER_SETTINGS.CLIENT_SECRET
)
auth = tweepy.OAuth1UserHandler(
    TWITTER_SETTINGS.CLIENT_ID,
    TWITTER_SETTINGS.CLIENT_SECRET
)