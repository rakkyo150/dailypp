import tweepy

import secret


def send_tweet(tweet_sentence, token, token_secret):
    auth = tweepy.OAuthHandler(secret.consumer_key, secret.consumer_secret, )
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)
    return api.update_status(tweet_sentence, wait_on_rate_limit=True)
