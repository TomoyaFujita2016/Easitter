#coding: utf-8
import tweepy 
import time
import random
import os
from tqdm import tqdm

def main(easitter, tags):
    print("MODE: follow")
    LIMIT = 300
    GET_PER = int(LIMIT / len(tags))
    followCnt = 0
    users = set()
    
    try:
        for tag in tags:
            # get and filter tweets
            tweets = easitter.searchTweets(tag, limit=GET_PER)
            filteredTweets, users = easitter.tweetsFiltering(tweets, users=users)

            for tweet in filteredTweets:
                #print(tweet.created_at)
                userId = tweet.user._json["id"]
                byFollow, message = easitter.byGoodUser(userId)
                if byFollow:
                    code, message = easitter.follow(userId)
                    if code == 1:
                        followCnt += 1 
                print("[%3d] " % followCnt + message)

    except tweepy.error.TweepError as tp:
        print(tp)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass
    print("\nFollow count: %4d" % followCnt)

