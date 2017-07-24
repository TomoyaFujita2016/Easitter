import byDestroy as byD
import byGoodUser as byG
import tweepy
import twitterApiSetup as tas
import sys
api = tas.tweetSetup()
me = api.me()
MyFriends = byD.getFriendsIds(api, me.id)
args = sys.argv
byLimit = False
FollowCnt = 0
FollowCntFromFriend= 0
#tags = ["絵かき","絵", "機械学習", "アプリ", "ゲーム", "ベンチャー", "強化学習", "アプリ開発","Android", "個人","院生", "帰宅", "個人開発", "DeepLearning", "学習結果"]
tags = ["機械学習", "Androidアプリ", "Androidゲームアプリ", "ベンチャー", "強化学習", "ゲームアプリ開発","AndroidStudio", "AndroidApp", "AndroidDeveloper", "個人開発", "DeepLearning"]
def byFollow(api, friend_id, lowerFFRatio, upperHashRatio, lowerTPDRatio, MyFriends):
    user = api.get_user(friend_id)
    if(byG.byAlreadyFriend(api, friend_id, MyFriends)):
        print("[ " + user.name + " ] is already followed!")
        return False
    if(not byG.byFFRatio(api, friend_id, lowerFFRatio)):
        print("[ " + user.name + " ] is a passive user!")
        return False
    if(byG.byBot(api, friend_id)):
        print("[ " + user.name + " ] is a bot!")
        return False
    if(byG.byCrazyHashTagUrl(api, friend_id, upperHashRatio)):
        print("[ " + user.name + " ] is a crazy hashtager!")
        return False
    if(byG.byOldMan(api, friend_id)):
        print("[ " + user.name + " ] is a old user!")
        return False
    return True
FollowCnt = 0
FollowCntFromFriend = 0
FollowLimit = 10

print("Start Following!")
while True:
    try:
        for tag in tags:
            for tweet in api.search(q=tag ,count=4):
                try:
                    if(byFollow(api, tweet.user.id, 0.75, 0.5, 0.25, MyFriends)):
                        api.create_friendship(tweet.user.id, True)
                        print("Successed in following " + tweet.user.name)
                        FollowCnt += 1
                        MyFriends.append(tweet.user.id)
                        if(FollowLimit <= (FollowCnt + FollowCntFromFriend)):
                            print("FollowLimit")
                            byLimit = True
                            raise Exception
                except tweepy.error.TweepError:
                    print("ERROR: FAILED TO FOLLOW "+ tweet.user.name)
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
    except Exception:
        if(byLimit):
            print ("\nCnt: "+ str(FollowCnt)+ "\nCntFromFriend: "+str(FollowCntFromFriend)+"\nTotal: "+str(FollowCnt+FollowCntFromFriend))
            break
        print("EXCEPTION OCCURED!!!")

