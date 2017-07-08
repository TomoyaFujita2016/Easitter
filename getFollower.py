import twitterApiSetup as tas
import tweepy

api = tas.tweetSetup()

friends = list()
for fd in tweepy.Cursor(api.friends).items():
    friends.append(fd)
    print (fd['User'])
