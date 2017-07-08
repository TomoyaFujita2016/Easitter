import tweepy
import twitterApiSetup as tas
import sys
api = tas.tweetSetup()

args = sys.argv
tags = ["絵描き", "機械学習", "強化学習", "ゲームアプリ開発","AndroidStudio", "AndroidApp", "AndroidDeveloper", "個人開発"]
for tag in tags:
    for tweet in api.search(q=tag, result_type='recent',count=100):
        try:
            api.create_friendship(tweet.user.id, True)
            print("Successed in following " + tweet.user.name)
        except tweepy.error.TweepError:
            print("ERROR: FAILED TO FOLLOW "+ tweet.user.name)

