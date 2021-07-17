import tweepy
import os


class Twitter_handler:
    def __init__(self,oauth_token, oauth_token_secret):
        global api
        auth = tweepy.OAuthHandler(os.environ['consumer_key'], os.environ['consumer_secret'], )
        auth.set_access_token(oauth_token, oauth_token_secret)
        api=tweepy.API(auth)

    def verify_credentials(self):
        return api.verify_credentials()

    def send_tweet(self,tweet_sentence):
        return api.update_status(tweet_sentence, wait_on_rate_limit=True)
