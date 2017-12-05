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
        tweets = easitter.getTimeline(limit=5000)
        filteredTweets, users = easitter.tweetsFiltering(tweets, users=users)

        for tweet in filteredTweets:
            code, message = easitter.favoriteTweet(tweetId=tweet.id)
            #print(tweet.text)
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
