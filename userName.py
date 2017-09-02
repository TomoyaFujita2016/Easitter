# coding: utf-8
import twitterApiSetup as tas
import tweepy
import sys
api = tas.tweetSetup()
args = sys.argv
for i in range(len(args)-2):
    usrId = args[i+2]
    user = api.get_user(usrId)
    if args[1] == "name":
        print(str(usrId) + " = " + user.name)
    elif args[1] == "id":
        print(str(usrId) + " = " + str(user.id))
    else:
        print("Please Input option!")
        print("python3 userName.py (id / name) --- --- ---")
        
