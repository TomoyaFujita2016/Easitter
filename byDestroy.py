import twitterApiSetup as tas
import datetime
from datetime import timedelta
import tweepy

def getFriendsIds(api, userId):
    friends_ids = []
    for friend_id in tweepy.Cursor(api.friends_ids, usr_id=userId).items():
        friends_ids.append(friend_id)
    return friends_ids

def getFollowersIds(api):
    try:
        my_info = api.me()
        followers_ids = []
        for follower_id in tweepy.Cursor(api.followers_ids, usr_id=my_info.id).items():
            followers_ids.append(follower_id)
        return followers_ids
    except tweepy.error.TweepError as terr:
        print("ERROR in getFollowersIds")

def byNotBeingFollowed(api, friend_id, followers_Ids):
    cnt = 0
    for follower_id in followers_Ids:
        if friend_id==follower_id:
            return False #IwasFollowed
        cnt += 1
    return True #Iwasnt Followed
def byOldMan(api, friend_id):

    limDate = datetime.datetime.today() - timedelta(days=28)
    try:
        userdata = api.get_user(id=friend_id)
        newestTweet = api.user_timeline(id=friend_id)[0]
        if newestTweet.created_at < limDate:
            return True
        else:
            return False
    except IndexError:
        print("This user has no tweets."+str(friend_id))
        return True
    except tweepy.error.TweepError:
        print ("ERROR: GET NEWEST TWEET FROM: " + str(friend_id))
        return False
