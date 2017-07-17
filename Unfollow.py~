import byDestroy as byD
import twitterApiSetup as tas
import tweepy

api = tas.tweetSetup()
me = api.me()
followers = byD.getFollowersIds(api)
friends = byD.getFriendsIds(api, me.id)

for friend in friends:
    if byD.byNotBeingFollowed(api, friend, followers):
        try:
            name = api.get_user(friend)
            api.destroy_friendship(friend)
            print ("Successed in unfollowing " + name.name)
        except tweepy.error.TweepError:
            print("ERROR: FAILED TO UNFOLLOW " + name.name)
