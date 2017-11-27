# coding: utf-8
from pyfiles import byDestroy as byD
from pyfiles import twitterApiSetup as tas
import os
import tweepy
from pyfiles import byGoodUser as byG

def byFollow(api, friend_id, lowerFFRatio, upperHashRatio, lowerTPDRatio, MyFriends):
    if not byD.byNotBeingFollowed(api, friend_id, followers):
        return True

    #if(byG.byAlreadyFriend(api, friend_id, MyFriends)):
        #print("[ " + str(friend_id) + " ] is already followed!")
        #return False
    #if(not byG.byFFRatio(api, friend_id, lowerFFRatio)):
        #print("[ " + str(friend_id) + " ] is a passive user!")
        #return False
    if(byG.byBot(api, friend_id)):
        print("[ " + str(friend_id) + " ] is a bot!")
        return False
    if(byG.byCrazyHashTagUrl(api, friend_id, upperHashRatio)):
        print("[ " + str(friend_id) + " ] is a crazy hashtager!")
        return False
    #if(byG.byOldMan(api, friend_id)):
        #print("[ " + str(friend_id) + " ] is a old user!")
        #return False
    return True

def main():    
    api = tas.tweetSetup()
    me = api.me()
    friends = byD.getFriendsIds(api, me.id)
    followers = byD.getFollowersIds(api)
    unfollowLimit =100
    UnfollowCnt = 0

    print("Started Unfollowing!")
    friends.reverse()
    for friend in friends:
        #if not(not byD.byNotBeingFollowed(api, friend, followers) and byFollow(api, friend, 0.75, 0.5, 0.25, friends)):
        if not(not byD.byNotBeingFollowed(api, friend, followers)):
            try:
                api.destroy_friendship(friend)
                UnfollowCnt += 1
                print (str(UnfollowCnt) + "Successed in unfollowing " + str(friend))
                if UnfollowCnt >= unfollowLimit:
                    print("UNFOLLOW LIMIT")
                    break
            except tweepy.error.TweepError:
                print("ERROR: FAILED TO UNFOLLOW " + str(friend))
        else:
            print("Didn't Unfollow " + str(friend))
    print('Unfollowing is done !')
    os.system('date')
