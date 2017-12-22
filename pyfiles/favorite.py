#coding: utf-8
import tweepy 
import time
import random
import os
from tqdm import tqdm

def main(easitter):
    print("MODE: favorite")
    tag = "#いいねした人全員フォローする"
    favoCnt = 0
    favoLimit = 1200
    users = set()
    
    try:
        # get and filter tweets
        tweets = easitter.searchTweets(tag, limit=favoLimit)
        filteredTweets, users = easitter.tweetsFiltering(tweets, users=users)

        for tweet in filteredTweets:
            if not tweet.retweeted and 'RT @' not in tweet.text:
                code, message = easitter.favoriteTweet(tweetId=tweet.id)

                #print(str(tweet.created_at))
                # favo restriction
                if code == 429:
                    print(message)
                    break
                print("[%3d] " % favoCnt + message)
                if code == 1:
                    favoCnt += 1

    except tweepy.error.TweepError as tp:
        print(tp)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass
    print("\nFavorite count: %4d" % favoCnt)

