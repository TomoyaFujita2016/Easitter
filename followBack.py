# coding: utf-8
import byDestroy as byD
import byGoodUser as byG
import tweepy
import twitterApiSetup as tas
import sys
import time
import random
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


print("Start Following Back!")
try:
    while True:
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
                time.sleep(1+ random.randint(2, 4))
        print("Zzzzzzz")
        time.sleep(60)
except KeyboardInterrupt:
    print("\nFINISH!")
    print("CNT: "+str(FollowCnt))
