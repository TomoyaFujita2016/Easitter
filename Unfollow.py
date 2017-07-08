import byDestroy as byD
import twitterApiSetup as tas
import tweepy

api = tas.tweetSetup()
followers = byD.getFollowersIds(api)
friends = byD.getFriendsIds(api)

for friend in friends:
    if byD.byNotBeingFollowed(api, friend, followers):
        try:
            api.destroy_friendship(friend)
            name = api.get_user(friend)
            print ("Successed in unfollowing " + name.name)
        except tweepy.error.TweepError:
            print("ERROR: FAILED TO UNFOLLOW " + name.name)
