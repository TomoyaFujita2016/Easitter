import byDestroy as byD
import tweepy
import twitterApiSetup as tas
import sys
api = tas.tweetSetup()
me = api.me()
args = sys.argv
FollowCnt = 0
FollowCntFromFriend= 0
tags = ["a","機械学習", "Androidアプリ", "Androidゲームアプリ", "ベンチャー", "強化学習", "ゲームアプリ開発","AndroidStudio", "AndroidApp", "AndroidDeveloper", "個人開発", "DeepLearning"]
while True:
    try:
        for tag in tags:
            for tweet in api.search(q=tag ,count=10):
                try:
                    api.create_friendship(tweet.user.id, True)
                    print("Successed in following " + tweet.user.name)
                    FollowCnt += 1
                except tweepy.error.TweepError:
                    print("ERROR: FAILED TO FOLLOW "+ tweet.user.name)
    
        MyFriends = byD.getFriendsIds(api, me.id)
        for myFriend in MyFriends:
            friends = byD.getFriendsIds(api, myFriend)
            for friend in friends:
                try:
                    name = api.get_user(friend)
                    api.create_friendship(friend, True)
                    FollowCntFromFriend += 1
                    print("Successed in following " + name.name)
                except tweepy.error.TweepError:
                    print("ERROR: FAILED TO FOLLOW "+ name.name)
    except KeyboardInterrupt:
        print ("Cnt: "+ str(FollowCnt)+ "\nCntFromFriend: "+str(FollowCntFromFriend)+"\nTotal: "+str(FollowCnt+FollowCntFromFriend))
        break
