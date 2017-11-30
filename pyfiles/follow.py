#coding: utf-8
from pyfiles import byDestroy as byD
from pyfiles import byGoodUser as byG
import tweepy
from pyfiles import twitterApiSetup as tas
import sys
def byFollow(api, friend_id, lowerFFRatio, upperHashRatio, lowerTPDRatio, MyFriends):
    #user = api.get_user(friend_id)
    
    if(byG.byAlreadyFriend(api, friend_id, MyFriends)):
        print("[ " +str(friend_id) + " ] is already followed!")
        return False
    if(not byG.byFFRatio(api, friend_id, lowerFFRatio)):
        print("[ " + str(friend_id) + " ] is a passive user!")
        return False
    if(byG.byBot(api, friend_id)):
        print("[ " + str(friend_id) + " ] is a bot!")
        return False
    if(byG.byCrazyHashTagUrl(api, friend_id, upperHashRatio)):
        print("[ " + str(friend_id) + " ] is a crazy hashtager!")
        return False
    if(byG.byOldMan(api, friend_id)):
        print("[ " + str(friend_id) + " ] is a old user!")
        return False
    return True
def main(tags):
    api = tas.tweetSetup()
    me = api.me()
    MyFriends = byD.getFriendsIds(api, me.id)
    args = sys.argv
    byLimit = False
    FollowCnt = 0
    FollowCntFromFriend= 0
    #tags = ["絵かき","絵", "機械学習", "アプリ", "ゲーム", "ベンチャー", "強化学習", "アプリ開発","Android", "個人","院生", "帰宅", "個人開発", "DeepLearning", "学習結果"]
    # tags = ["機械学習", "強化学習", "卒論" ,"Androidアプリ", "Androidゲームアプリ", "ゲームアプリ開発","AndroidStudio", "AndroidApp", "AndroidDeveloper", "個人開発", "DeepLearning"]
    
    FollowCnt = 0
    FollowCntFromFriend = 0
    FollowLimit = 100
    
    print("Start Following!")
    while True:
        try:
            for tag in tags:
                for tweet in api.search(q=tag ,count=9):
                    try:
                        if(byFollow(api, tweet.user.id, 0.5, 0.5, 0.25, MyFriends)):
                            api.create_friendship(tweet.user.id, True)
                            print("Successed in following " + tweet.user.name)
                            FollowCnt += 1
                            MyFriends.append(tweet.user.id)
                            if(FollowLimit <= (FollowCnt + FollowCntFromFriend)):
                                print("FollowLimit")
                                byLimit = True
                                raise Exception
                    except tweepy.error.TweepError as twp:
                        print("ERROR: FAILED TO FOLLOW "+ tweet.user.name)
                        print(twp)
            '''            
            MyFriends = byD.getFriendsIds(api, me.id)
            for myFriend in MyFriends:
                friends = byD.getFriendsIds(api, myFriend)
                for friend in friends:
                    try:
                        name = api.get_user(friend)
                        if(byFollow(api, friend, 0.75, 0.5, 0.25, MyFriends)):
                            api.create_friendship(friend, True)
                            FollowCntFromFriend += 1
                            MyFriends.append(friend)
                            print("Successed in following " + name.name)
                            if(FollowLimit <= (FollowCnt + FollowCntFromFriend)):
                                print("FollowLimit")
                                raise Exception
                    except tweepy.error.TweepError:
                        print("ERROR: FAILED TO FOLLOW "+ name.name)
            '''
        except KeyboardInterrupt:
            print ("\nCnt: "+ str(FollowCnt)+ "\nCntFromFriend: "+str(FollowCntFromFriend)+"\nTotal: "+str(FollowCnt+FollowCntFromFriend))
            break
        except Exception as e:
            if(byLimit):
                print ("\nCnt: "+ str(FollowCnt)+ "\nCntFromFriend: "+str(FollowCntFromFriend)+"\nTotal: "+str(FollowCnt+FollowCntFromFriend))
                break
            print("EXCEPTION OCCURED!!!")
            print(e)
