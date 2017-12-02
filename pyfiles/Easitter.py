# encoding: utf-8
# author: Tomoya
# created_at: 2017/12/01
import tweepy
import datetime
from datetime import timedelta
import os
from tqdm import tqdm
import re

class Easitter(object):
    CK = "warrm7a0cjWy62GbnjQRLUXtd"
    CS = "56CITHgkJyhx824WlYyM8lgp4sBE2M6j1bo4PfxXBY4Oti1Cz5"
    AT = "883630081473617921-5EHbdHAPn7MURLhFtD0uewHvMQPs3X2"
    AS = "0ObJeBCW2yszFr8elB8PDGxi24JEoVpxmTSAbELucy9oe"

    SAMPLE_NUM = 100
    # if it's 1.0, ex) follow=100 and follower=0
    # if it's 0.5, ex) follow=100 and follower=100
    # if it's 0.25 ex) follow=33 and follower=100
    MIN_FRIENDS_RATIO = 0.35
    # 1 month
    MAX_DAY_SPAN = 7*4
    # if it's 1.0, all tweets have url or hashtag
    MIN_HASHURL_RATIO = 0.5

    def __init__(self, CK=CK,CS=CS,AT=AT,AS=AS):
        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AT, AS)

        self.API = tweepy.API(auth, api_root='/1.1', wait_on_rate_limit=True)
        self.ME = self._getMe()

    def _getMe(self):
        return self.API.me()
    
    def _getTweetId(self, tweet):
        return tweet.id

    def _getUser(self, userId):
        return self.API.get_user(userId)
    
    def _byProtected(self, userId):
        user = _getUser(userId)
        return user.protected
    
    def _getNewestTweetId(self, tag, maxId=None):
        if maxId is None:
            tweet = self.API.search(q=tag, count=1)
        else:
            tweet = self.API.search(q=tag, count=1, max_id=maxId)
        if len(tweet) == 0:
            return 0, 0
        return tweet, tweet[-1].id

    def byInclude(self, words, target):
        if type(words) == list:
            for word in words:
                if word in target:
                    return True
            return False
        if words in target:
            return True
        return False

    def byGoodUser(self, userId):
        # Whether the user follows me or not
        if not self.byFollowedMe(userId):
            return False
        # Whether the user's last tweet is old or not
        if MAX_DAY_SPAN < self.getDaySpan(userId):
            return False
        # Whether the user's tweets have url or hash tag
        if MIN_HASHURL_RATIO < self.getHashUrlRatio(userId):
            return False
        # Whether the user is a bot or not
        if self.byBot(userId):
            return False
        # Whether the user tweet frequently or not
        #if MIN_TWEET_PER_DAY > self.getTweetPerDay(userId):
            #return False
        return True

    def getDaySpan(self, userId):
        lastTweet = self.getTweets(userId, limit=1)
        if len(lastTweet) == 0:
            # Too long ??
            return 365*8
        newestDate = lastTweet.created_at
        span = datetime.datetime.today() - newestDate
        return span.days


    def getUserData(self, userId):    
        try:
            user = self._getUser(userId)
            name = user.name
            friendsCnt = user.friends_count
            followersCnt = user.followers_count
            tweetCnt = user.statuses_count
            createdAt = user.created_at
            return locals()
        except tweepy.error.TweepError as et:
            print(et)
            return {}
    
    # Too old tweet is inefficiency to increase followers, so I made pageNum 5.
    def searchTweets(self, tag, pageNum=5, maxIdOrg=None):
        try:
            if maxIdOrg is None:
                newestTweet, maxId = self._getNewestTweetId(tag)
            else:
                maxId = maxIdOrg
                newestTweet, maxId = self._getNewestTweetId(tag, maxId=maxIdOrg)
            
            if type(newestTweet) is int:
                return [], None
            searchedTweets = [newestTweet]
            pBar = tqdm(range(pageNum))
            for page in pBar:
                pBar.set_description("PAGE:[%2d/%2d] Getting Tweets !" % (page+1, pageNum))
                tweets = self.API.search(q=tag, count=100, max_id=maxId-1)
                if len(tweets) == 0:
                    break
                searchedTweets.extend(tweets[::-1])
                maxId = tweets[-1].id
        except tweepy.error.TweepError as et:
            print(et)
        except Exception as e:
            print(e)
        print("%d Tweets was gotten !" % len(searchedTweets))
        # first index has SearchResult Object
        return searchedTweets[1:], maxId
    
    # if the tweets has more than 2 tweet which is tweeted by same user, it delete old tweet.
    def tweetsFiltering(self, tweets, users=set()): 
        filteredTweets = []
        userList = set()
        userList |= users
        try:
            for tweet in tweets[::-1]:
                if not tweet.user.screen_name in userList:
                    filteredTweets.append(tweet)
                    userList.add(tweet.user.screen_name)
            return filteredTweets, userList
        except tweepy.error.TweepError as et:
            print(et)
        except Exception as e:
            print(e)
    def getUserTimeline(self, userId, limit=200):
        tweets = []
        try:
            tweetsObj = tweepy.Cursor(self.API.user_timeline, id=userId).items(200)
            for cnt, tweet in enumerate(tweets):
                if not cnt < limit:
                    break
                tweets.append(tweet)
        except tweepy.error.TweepError as et:
            print(et)
        return tweets

    def getFriendIds(self, screenName, limit=5000):
        if self._byProtected(screenName):
            return []
        friendIds = []
        try:
            friends = tweepy.Cursor(\
                    self.API.friends_ids,\
                    id = screenName, \
                    cursor = -1\
                    ).items()
            for cnt, friend in enumerate(friends):
                if not cnt < limit:
                    break
                friendIds.append(friend)
            return friendIds
        except tweepy.error.TweepError as et:
            print(et)
            return []

    def getFollowerIds(self, screenName, limit=5000):
        if self._byProtected(screenName):
            return []
        followerIds = []
        try:
            followers = tweepy.Cursor(\
                    self.API.followers_ids,\
                    id = screenName, \
                    cursor = -1\
                    ).items()
            for cnt, follower in enumerate(followers):
                if not cnt < limit:
                    break
                followerIds.append(follower)
        except tweepy.error.TweepError as et:
            print(et)
            return []
        return followerIds
    
    def getTweetData(self, tweet):
        try:
            tweetText = tweet.text
            tweetFavo = tweet.favorite_count
            tweetRet = tweet.retweet_count
        except tweepy.error.TweepError as et:
            print(et)
            return "", "", ""
        return tweetText, tweetFavo, tweetRet

    def getTweets(self, screenName, limit=200):
        tweets = []
        try:
            tweetsObj = tweepy.Cursor( \
                    self.API.user_timeline, \
                    screen_name=screenName, \
                    exclude_replies = True \
                    ).items()
            for cnt, tweet in enumerate(tweetsObj):
                if not cnt < limit:
                    break
                tweets.append(tweet)
        except tweepy.error.TweepError as et:
            print(et)
            return []
        return tweets
    
    def favoriteTweet(self, tweetId=None, tweet=None):
        if not tweetId is None and not tweet is None:
            return False 
        if not tweet is None:
            tId = self._getTweetId(tweet)
        if not tweetId is None:
            tId = tweetId
        try:
            self.API.create_favorite(tId)
            return 1, "Succeed in favoritting this tweet!"
        
        except tweepy.error.TweepError as tp:    
            #print(type(tp.reason))
            erL = self.arrangeListStr(tp.reason)
            return int(erL[1]), erL[3]

    def follow(self, userId):
        try:
            self.API.create_friendship(userId, True)
        except tweepy.error.TweepError as tp:
            print(tp)
    
    def getFriendShip(self, obsUserId, tarUserId):
        # if obsUser follows tarUser, it returns True
        return self.API.exists_friendship(obsUserId, tarUserId)
    
    def byFollowedMe(self, userId):
        return self.getFriendShip(userId,self._getMe())

    def getTweetPerDay(self, userId):
        today = datetime.datetime.today()
        userData = self.getUserData(userId)
        days = (today - userData["createdAt"]).days
        tweetAmount = userData["tweetCnt"]
        tweetPerDay = tweetAmount/days
        return tweetPerDay
    
    def byHashOrUrl(self, tweet):
        NG_LIST = ["#", "http", "/"]
        return self._byInclude(NG_LIST, target)
    
    def getHashUrlRatio(self, userId):
        tweets = self.getTweetData(userId, limit=SAMPLE_NUM)
        hashUrlCnt = 0
        for tweet in tweets:
            if self.byHashOrUrl(tweet):
                hashUrlCnt += 1
        return hashUrlCnt / len(tweets)

    def byBot(self, userId):
        NG_LIST = ["まとめ", "bot", "Bot", "BOT"]
        user = self._getUser(userId)
        return self._byInclude(NG_LIST, user.name)

    def getFriendRatio(self, userId):
        userData = self.getUserData(userId)
        friendsNum = userData["friendsCnt"]
        followersNum = userData["followersCnt"]
        if (followersNum + friendsNum) == 0:
            return 1
        return friendsNum / (followersNum + friendsNum)

    def arrangeListStr(self, strList):
        REP_LIST = ["[", "]", "'", "‘", "’", "{", "}"]
        SP_LIST = "[,:]"
        tmpStrList = []
        if type(strList) == str:
            tmpStrList.append(strList)
        else:
            tmpStrList = strList[:]
        for i, val in enumerate(tmpStrList):
            for rep in REP_LIST:
                val = val.replace(rep, "")
            tmpStrList[i] = re.split(SP_LIST, val)
        if len(tmpStrList) == 1:
            return tmpStrList[0]
        return tmpStrList
    
