import tweepy
import twitterApiSetup as tas
import time
import random
api = tas.tweetSetup()
byManyError = False
favoCnt = 0
errorCnt = 0
manyErrorCnt = 0
Cnt = 0
tags = ["#いいねした人全員フォローする"]
#tags = ["#全員フォローする"]
print("Let's Favorite !!")
while True:
    try:
        for tweet in api.search(q=tags, count=100):
            try:
                api.create_favorite(tweet.id)
                print("Successed in favoritting this tweet !("+str(favoCnt + 1) +") id: "+ str(tweet.id))
                favoCnt += 1
                errorCnt = 0
                manyErrorCnt = 0

            except tweepy.error.TweepError as terr:
                print("ERROR: FAILED TO FAVORITE!("+str(errorCnt)+") name:"+ tweet.user.name + " id:"+str(tweet.id))
                print(terr)
                errorCnt += 1
            except Exception:
                print("ERROR OCCUERD!!("+str(errorCnt)+")")
                errorCnt += 1
            if(((Cnt != 0)and(Cnt % 140 == 0)) or (errorCnt >= 10)):
                if(errorCnt >= 10):
                    byManyError = True
                errorCnt = 0
                print("Zzzzzzzz.....")
                #901
                time.sleep(900)
                byFirst = True
            Cnt += 1
            if(byManyError):
                byManyError = False
                manyErrorCnt += 1
                print("ManyError: back to start tweet")
                break
            if(manyErrorCnt >= 2):
                print("TOO MANY ERRORS !!")
                raise KeyboardInterrupt
            time.sleep(1 + random.randint(0,1))

            
            
    except KeyboardInterrupt:
        print("\nFAVO COUNT: "+ str(favoCnt))
        break
