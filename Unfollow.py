import byDestroy as byD
import twitterApiSetup as tas
import tweepy
import byGoodUser as byG

api = tas.tweetSetup()
me = api.me()
friends = byD.getFriendsIds(api, me.id)
followers = byD.getFollowersIds(api)
def byFollow(api, friend_id, lowerFFRatio, upperHashRatio, lowerTPDRatio, MyFriends):
    user = api.get_user(friend_id)
    if not byD.byNotBeingFollowed(api, friend_id, followers):
        return True

    #if(byG.byAlreadyFriend(api, friend_id, MyFriends)):
        #print("[ " + user.name + " ] is already followed!")
        #return False
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
print("Started Unfollowing!")
friends.reverse()
for friend in friends:
    name = api.get_user(friend)
    if not(byFollow(api, friend, 0.75, 0.5, 0.25, friends)):
        try:
            api.destroy_friendship(friend)
            UnfollowCnt += 1
            print (str(UnfollowCnt) + "Successed in unfollowing " + name.name)
            if UnfollowCnt == -1:
                print("UNFOLLOW LIMIT")
                break
        except tweepy.error.TweepError:
            print("ERROR: FAILED TO UNFOLLOW " + name.name)
    else:
        print("Didn't Unfollow " + name.name)
