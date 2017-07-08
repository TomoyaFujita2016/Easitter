import twitterApiSetup as tas
import datetime
from datetime import timedelta
import tweepy

api = tas.tweetSetup()

def getFriendsIds(api):
    my_info = api.me()
    friends_ids = []
    for friend_id in tweepy.Cursor(api.friends_ids, usr_id=my_info.id).items():
        friends_ids.append(friend_id)
    return friends_ids

def getFollowersIds(api):
    my_info = api.me()
    followers_ids = []
    for follower_id in tweepy.Cursor(api.followers_ids, usr_id=my_info.id).items():
        followers_ids.append(follower_id)
        print("HELLO")
    return followers_ids

def byNotBeingFollowed(api, friend_id, followers_Ids):
    cnt = 0
    for follower_id in followers_Ids:
        if friend_id==follower_id:
            break
        cnt += 1
    if cnt == len(followers_Ids):
        return True
    else:
        return False

def byOldMan(api, friend_id):

    limDate = datetime.datetime.today() - timedelta(days=28)
    userdata = api.get_user(id=friend_id)
    try:
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
def byDestroyFriendShip(api, friends_Ids, followers_Ids):
    
    #Whether it is being followed or not
    for friend_id in friends_Ids:
        cnt = 0
        for follower_id in followers_Ids:
            if friend_id==follower_id:
                break
            cnt += 1
        if cnt == len(followers_Ids):
            byNotBeingFollowed = True
        else:
            byNotBeingFollowed = False
        print ("NOTBEINGFOLLOWED: "+ str(byNotBeingFollowed))

    #Newest Tweet Date > 4weeks ago
    limDate = datetime.datetime.today() - timedelta(days=28)
    for friend_id in friends_Ids:
        userdata = api.get_user(id=friend_id)
        try:
            newestTweet = api.user_timeline(id=friend_id)[0]
            if newestTweet.created_at < limDate:
                byOldMan = True
            else:
                byOldMan = False
        except IndexError:
            byOldMan = True
        except tweepy.error.TweepError:
            print ("ERROR: GET NEWEST TWEET FROM: " + str(friend_id))
        print ("byOldMan: " + str(byOldMan))

getFollowersIds(api)
for friend in getFriendsIds(api):
    #byOldMan(api, friend)
    print(str(byNotBeingFollowed(api, friend, getFollowersIds(api))))
