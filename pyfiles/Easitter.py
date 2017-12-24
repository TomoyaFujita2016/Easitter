# encoding: utf-8
# author: Tomoya
# created_at: 2017/12/01
import tweepy
import datetime
from datetime import timedelta
from datetime import datetime as dtdt
import datetime as dt
import os
from tqdm import tqdm
import re
import pickle as pkl

class Easitter(object):
    CK = "warrm7a0cjWy62GbnjQRLUXtd"
    CS = "56CITHgkJyhx824WlYyM8lgp4sBE2M6j1bo4PfxXBY4Oti1Cz5"
    AT = ""
    AS = ""

    def __init__(self, CK=CK,CS=CS,AT=AT,AS=AS, byGetF=True):
        self.SAMPLE_NUM = 50
        # if it's 1.0, ex) follow=100 and follower=0
        # if it's 0.5, ex) follow=100 and follower=100
        # if it's 0.25 ex) follow=33 and follower=100
        self.MIN_FRIENDS_RATIO = 0.35
        # 1 month
        self.MAX_DAY_SPAN = 7*4.
        # if it's 1.0, all tweets have url or hashtag
        self.MIN_HASHURL_RATIO = 0.55
        
        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AT, AS)

        self.API = tweepy.API(auth, api_root='/1.1', wait_on_rate_limit=True)
        self.ME = self._getMe()
        
        if byGetF:
            # self.friends is not used now
            # self.friends = self.getFriendIds(self.ME)
            self.friends = []
            self.followers = self.getFollowerIds(self.ME)

    def _getMe(self):
        return self.API.me().id
    
    def _getTweetId(self, tweet):
        return tweet.id

    def _getUser(self, userId):
        return self.API.get_user(userId)
    
    def _byProtected(self, userId):
        user = self._getUser(userId)
        return user.protected
    
    def _getNewestTweetId(self, tag, maxId=None):
        if maxId is None:
            tweet = self.API.search(q=tag, count=1)
        else:
            tweet = self.API.search(q=tag, count=1, max_id=maxId)
        if len(tweet) == 0:
            return 0, 0
        return tweet, tweet[-1].id
    
    def getUsername(self, userId):
        return self._getUser(userId).screen_name


    def byInclude(self, words, target):
        if type(words) == list:
            for word in words:
                if word in target:
                    return True
            return False
        if words in target:
            return True
        return False
    
    def byFollowBack(self, userId):
        # Whether the user follows me or not
        if not self.byFollowedMe(userId):
            return False, "caused by Being NOT Followed!"
        # Whether the user's last tweet is old or not
        span = self.getDaySpan(userId)
        if self.MAX_DAY_SPAN < span:
            return False, "caused by Old User! " + str(span)
        # Whether the user's tweets have url or hash tag
        huRatio = self.getHashUrlRatio(userId)
        if self.MIN_HASHURL_RATIO < huRatio:
            return False, "caused by Crazy Hash Tagger! " + str(huRatio)
        # Whether the user is a bot or not
        if self.byBot(userId):
            return False, "caused by Bot!"
        # Whether the user tweet frequently or not
        #if MIN_TWEET_PER_DAY > self.getTweetPerDay(userId):
            #return False
        return True, ""

    def byGoodUser(self, userId):
        # Whether the user's last tweet is old or not
        #print(str(self.getDaySpan(userId)))
        #if self.MAX_DAY_SPAN < self.getDaySpan(userId):
        #    print(" old user")
        #    return False, "Old User!"
        # Whether the user's tweets have url or hash tag
        if self.MIN_HASHURL_RATIO < self.getHashUrlRatio(userId):
            return False, "caused by Crazy Hash Tagger!"
        # Whether the user is a bot or not
        if self.byBot(userId):
            return False, "caused by Bot !"
        # Whether the user tweet frequently or not
        #if MIN_TWEET_PER_DAY > self.getTweetPerDay(userId):
            #return False
        return True, ""

    def getDaySpan(self, userId):
        try:
            lastTweet = self.getTweets(userId, limit=1)
            if len(lastTweet) == 0:
                # Too long ??
                return 365*8
            newestDate = lastTweet[0].created_at
            #print(str(newestDate) + " / " + str(datetime.datetime.today()))
            span = datetime.datetime.today() - newestDate
            #print("Days: " + str(span.days))
            return span.days
        except Exception as e:
            print(e)
        except tweepy.error.TweepError as e:
            print(e)

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

    def getTimeline(self, limit=50000, resultType="recent"):
        try:
            tweets = []
            tweetsObj = tweepy.Cursor(self.API.home_timeline,
                    result_type=resultType,
                    exclude_replies = False).items(limit)
            
            pBar = tqdm(tweetsObj, ascii=True, total=limit, desc="Getting Tweets!")
            for cnt, tweet in enumerate(pBar):
                pBar.update(1)
                if not cnt < limit:
                    break
                tweets.append(tweet)
        except tweepy.error.TweepError as et:
            print(et)
        except Exception as e:
            print(e)
        return tweets

    def searchTweets(self, tag, limit=50000, tfilter=" -filter:retweets", resultType="recent"):
        # if tfilter is appended to tag, it'll have some problem about tqdm, or what???.
        # I don't know why it'll have the problem.
        #tag += tfilter
        try:
            tweets = []
            tweetsObj = tweepy.Cursor(self.API.search, 
                    q=tag, 
                    result_type=resultType,
                    exclude_replies = True).items(limit)
            
            pBar = tqdm(tweetsObj, ascii=True, total=limit, desc="Getting Tweets!")
            for cnt, tweet in enumerate(pBar):
                pBar.update(1)
                if not cnt < limit:
                    break
                tweets.append(tweet)
        except tweepy.error.TweepError as et:
            print(et)
        except Exception as e:
            print(e)
        return tweets
    
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

    def getFriendIds(self, userId, limit=100000):
        if self._byProtected(userId):
            return []
        friendIds = []
        try:
            friends = tweepy.Cursor(\
                    self.API.friends_ids,\
                    user_id = userId, \
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

    def getFollowerIds(self, userId, limit=5000):
        if self._byProtected(userId):
            return []
        followerIds = []
        try:
            followers = tweepy.Cursor(\
                    self.API.followers_ids,\
                    user_id = userId, \
                    cursor = -1).items()
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

    def getTweets(self, userId, limit=50):
        tweets = []
        try:
            tweetsObj = tweepy.Cursor( \
                    self.API.user_timeline, \
                    user_id=userId, \
                    exclude_replies = True \
                    ).items(limit)
            for cnt, tweet in enumerate(tweetsObj):
                if not cnt < limit:
                    break
                # print(tweet.text.replace("\n", ""))
                tweets.append(tweet)
        except tweepy.error.TweepError as et:
            print(et)
        
        return tweets
    
    def favoriteTweet(self, tweetId=None, tweet=None):
        if not tweetId is None and not tweet is None:
            return False 
        if not tweet is None:
            tId = self._getTweetId(tweet)
        elif not tweetId is None:
            tId = tweetId
        else:
            print("please input a tweet id")
        try:
            self.API.create_favorite(tId)
            return 1, "Succeed in favoritting this tweet! %d"%tId
        
        except tweepy.error.TweepError as tp:    
            #print(type(tp.reason))
            if "429" in tp.reason:
                return 429, "Favo restriction! %d"%tId
            if "139" in tp.reason:
                return 139, "You have already favorite it! %d"%tId
            return -1, "Exception! %s"%str(tp.reason)

    def follow(self, userId):
        try:
            #self.API.create_friendship(userId, True)
            #self._getUser(userId).follow()
            self.API.create_friendship(userId, True)
            self.friends.append(userId)
            return 1, "Succeed in follow " + self.getUsername(userId)
        except tweepy.error.TweepError as tp:
            return -1, tp.reason+ " " + self.getUsername(userId)
    
    def unfollow(self, userId):
        try:
            #self.API.create_friendship(userId, True)
            #self._getUser(userId).follow()
            self.API.destroy_friendship(userId, True)
            return 1, "Succeed in unfollow " + self.getUsername(userId)
        except tweepy.error.TweepError as tp:
            return -1, tp.reason+ " " + self.getUsername(userId)
    
    def getFriendShip(self, obsUserId, tarUserId):
        # if obsUser follows tarUser, it returns True
        followersIds = self.getFollowerIds(tarUserId)
        return (obsUserId in followersIds)
    
    def byFollowedMe(self, userId):
        return userId in self.followers

    def getTweetPerDay(self, userId):
        today = datetime.datetime.today()
        userData = self.getUserData(userId)
        days = (today - userData["createdAt"]).days
        tweetAmount = userData["tweetCnt"]
        tweetPerDay = tweetAmount/days
        return tweetPerDay
    
    def byHashOrUrl(self, tweet):
        NG_LIST = ["#", "http", "/"]
        return self.byInclude(NG_LIST, tweet)
    
    def getHashUrlRatio(self, userId):
        tweets = self.getTweets(userId, limit=self.SAMPLE_NUM)
        hashUrlCnt = 0
        try:
            for tweet in tweets:
                if self.byHashOrUrl(tweet.text):
                   hashUrlCnt += 1
        except Exception as e:
            print(e)
        return hashUrlCnt / len(tweets)

    def byBot(self, userId):
        NG_LIST = ["まとめ", "bot", "Bot", "BOT"]
        user = self._getUser(userId)
        return self.byInclude(NG_LIST, user.name)

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
    
    def confirmPklFile(self, path): 
        if os.path.exists(path): 
            with open(path, "rb") as f:
                return pkl.load(f)
        else:
            return []
    
    def savePklFile(self, path, data):
        dirPath = path.split("/")
        if 1 < len(dirPath):
            dirPath = "/".join(list(dirPath)[0:-1]) + "/"
            os.makedirs(dirPath, exist_ok=True)

        with open(path, "wb") as f:
            pkl.dump(data, f)
    def getMention(self, limit=100, befDays=-7):
        tweets = []
        date = self.getDate(befDays)
        replys = self.API.mentions_timeline(count=100)
        for status in replys:
            # print("date " + date)
            # print("created " + str(status.created_at).split(" ")[0])
            if not date < str(status.created_at).split(" ")[0]:
                break
            tweets.append(status)
        return tweets

    def getDate(self, addDay):
        # ex) '12-20-31'
        return str(dtdt.now() + dt.timedelta(days=addDay)).split(" ")[0]
          
    def tweet(self, message, reply=None):
        # reply is reply status id
        try:
            if reply is None:
                self.API.update_status(status=message)
            else:
                self.API.update_status(status=message, in_reply_to_status_id=reply)
            return "Succeeded in tweet: %s" % message

        except tweepy.error.TweepError as e:
            return "Failed to tweet: %s" % str(e.reason)



