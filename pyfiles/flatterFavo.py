#coding: utf-8
import tweepy 
import time
import random
import os
from tqdm import tqdm

def main(easitter):
    print("MODE: flattering")
    favoCnt = 0
    me = easitter.ME
    users = set()
    users.add(me)
    
    try:
        # get and filter tweets
        tweets = easitter.getUserTimeline(me, limit=10)
        filteredTweets, users = easitter.tweetsFiltering(tweets, users=users)

        for tweet in tweets:
            code, message = easitter.favoriteTweet(tweetId=tweet.id)
            
            # favo restriction
            if code == 429:
                print(message)
            if code == 1:
                favoCnt += 1
            
            print("[%3d] " % favoCnt + message)

    except tweepy.error.TweepError as tp:
        print(tp)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass
    print("\nFlattering count: %4d" % favoCnt)
