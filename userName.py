# coding: utf-8
import twitterApiSetup as tas
import tweepy
import sys
api = tas.tweetSetup()
args = sys.argv
for i in range(len(args)-1):
    usrId = args[i+1]
    user = api.get_user(usrId)
    print(str(usrId) + " = " + user.name) 
