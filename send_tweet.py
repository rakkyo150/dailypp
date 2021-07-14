import tweepy
import os

def send_tweet(tweet_sentence, token, token_secret):
    auth = tweepy.OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret'], )
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)
    return api.update_status(tweet_sentence, wait_on_rate_limit=True)
