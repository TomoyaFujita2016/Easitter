import byDestroy as byD
import twitterApiSetup as tas
import tweepy

api = tas.tweetSetup()
me = api.me()
followers = byD.getFollowersIds(api)
friends = byD.getFriendsIds(api, me.id)
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
UnfollowCnt = 0
for friend in friends:
    if not byFollow(api, friend, 0.75, 0.5, 0.25, friends):
        try:
            name = api.get_user(friend)
            api.destroy_friendship(friend)
            UnfollowCnt += 1
            if UnfollowCnt == 80:
                print("UNFOLLOW LIMIT")
                break
            print ("Successed in unfollowing " + name.name)
        except tweepy.error.TweepError:
            print("ERROR: FAILED TO UNFOLLOW " + name.name)
