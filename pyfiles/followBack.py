# coding: utf-8
from pyfiles import byDestroy as byD
from pyfiles import byGoodUser as byG
import tweepy
from pyfiles import twitterApiSetup as tas
import sys
import os
import time
import random

def byFollow(api, friend_id, upperHashRatio,  MyFriends):
    if(byG.byAlreadyFriend(api, friend_id, MyFriends)):
        print("[ " + str(friend_id) + " ] is already followed!")
        return False
    if(byG.byBot(api, friend_id)):
        print("[ " + str(friend_id) + " ] is a bot!")
        return False
    if(byG.byCrazyHashTagUrl(api, friend_id, upperHashRatio)):
        print("[ " + str(friend_id) + " ] is a crazy hashtager!")
        return False
    return True

def main():
    api = tas.tweetSetup()
    me = api.me()
    MyFollowers_id = byD.getFollowersIds(api)
    MyFriends_id = byD.getFriendsIds(api, me.id)
    args = sys.argv
    byLimit = False
    FollowCnt = 0
    FollowCntFromFriend = 0
    FollowLimit = 350
    #MyFollowers_id.reverse()
    
    print("Start Following Back!")
    try:
        for MyFollower in MyFollowers_id:
            if(not byD.byNotBeingFollowed(api, MyFollower, MyFollowers_id) and byFollow(api, MyFollower, 0.35,  MyFriends_id)):
                try:
                    api.create_friendship(MyFollower, True)
                    print("(" + str(FollowCnt + 1)  +")Successed in following back " + str(MyFollower))
                    MyFriends_id.append(MyFollower)
                    FollowCnt += 1
                except tweepy.error.TweepError as TER:
                    print("FAILED TO FOLLOW BACK "+ str(MyFollower))
                    print(TER)
                if(FollowLimit <= FollowCnt):
                    print("FollowLimit!")
                    raise KeyboardInterrupt
                time.sleep(1+ random.randint(1, 2))
        print("Zzzzzzz")
        time.sleep(60)
    except KeyboardInterrupt:
        print("\nFollowing Back is done !")
        os.system('date')
        print("CNT: "+str(FollowCnt))
