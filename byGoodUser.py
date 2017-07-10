
def byFFRatio(api, friend_id, lowerFFRatio):
    user = api.get_user(friend_id)
    friendsCount = user.friends_count
    followersCount = user.followers_count
    ffRatio = friendsCount / followersCount
    if(lowerFFRatio < ffRatio):
        return True
    return False

def byBot(api, friend_id):
    user = api.get_user(friend_id)
    name = user.name
    return ('bot' in name) or ('Bot' in name) or ('BOT' in name)

def byCrazyHashTag(api, friend_id, upperHashRatio):
    import tweepy
    amountOfTweet = 80
    hashCount = 0
    try:
        for tweet in tweepy.Cursor(api.user_timeline, id=friend_id).items(amountOfTweet):
            if('#' in tweet.text):
                hashCount += 1
    except tweepy.error.TweepError:
        user = api.get_user(friend_id)
        print("ERROR: FAILED TO GET TWEET FROM" + user.name)
        return True

    hashRatio = hashCount / amountOfTweet
    if(upperHashRatio < hashRatio):
        return True

    return False

def byOldMan(api, friend_id):
    import datetime
    from datetime import timedelta
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
        return True

def byTweetPerDay(api, friend_id, lowerTPDRatio):
    import datetime
    from datetime import timedelta

    today = datetime.datetime.today()
    user = api.get_user(friend_id)
    days = today - user.created_at
    amountOfTweets = user.statuses_count
    tweetPerDay = amountOfTweets / days.days

    if(lowerTPDRatio < tweetPerDay):
        return True
    return False
