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
FollowLimit = 100

def byFollow(api, friend_id, upperHashRatio,  MyFriends):
    user = api.get_user(friend_id)
    if(byG.byAlreadyFriend(api, friend_id, MyFriends)):
        print("[ " + user.name + " ] is already followed!")
        return False
    if(byG.byBot(api, friend_id)):
        print("[ " + user.name + " ] is a bot!")
        return False
    if(byG.byCrazyHashTagUrl(api, friend_id, upperHashRatio)):
        print("[ " + user.name + " ] is a crazy hashtager!")
        return False
    return True


print("Start Following Back!")
try:
    for MyFollower in MyFollowers_id:
        user = api.get_user(MyFollower)
        if(byFollow(api, MyFollower, 0.35,  MyFriends_id) and not byD.byNotBeingFollowed(api, MyFollower, MyFollowers_id)):
            try:
                api.create_friendship(MyFollower, True)
                print("(" + str(FollowCnt + 1)  +")Successed in following back " + user.name)
                MyFriends_id.append(MyFollower)
                FollowCnt += 1
            except tweepy.error.TweepError as TER:
                print("FAILED TO FOLLOW BACK "+ user.name)
                print(TER)
            if(FollowLimit <= FollowCnt):
                print("FollowLimit!")
                break
            time.sleep(1+ random.randint(0, 2))
except KeyboardInterrupt:
    print("\nFINISH!")
    print("CNT: "+str(FollowCnt))
