import tweepy
import twitterApiSetup as tas
import time
import random
api = tas.tweetSetup()
favoCnt = 0
errorCnt = 0
Cnt = 0
#tags = ["#いいねした人全員フォローする"]
tags = ["#全員フォローする"]
print("Let's Favorite !!")
while True:
    try:
        for tweet in api.search(q=tags, count=100):
            try:
                api.create_favorite(tweet.id)
                #tweet.favorite
                print("Successed in favoritting this tweet !("+str(favoCnt + 1) +") id: "+ str(tweet.id))
                favoCnt += 1
                errorCnt = 0

            except tweepy.error.TweepError as terr:
                print("ERROR: FAILED TO FAVORITE!("+str(errorCnt)+") name:"+ tweet.user.name + " id:"+str(tweet.id))
                print(terr)
                errorCnt += 1
            except Exception:
                print("ERROR OCCUERD!!("+str(errorCnt)+")")
                errorCnt += 1
            if(((Cnt != 0)and(Cnt % 40 == 0)) or (errorCnt >= 10)):
                errorCnt = 0
                print("Zzzzzzzz.....")
                #901
                time.sleep(30)
                byFirst = True
            Cnt += 1
            time.sleep(2 + random.randint(1,3))
            
    except KeyboardInterrupt:
        print("\nFAVO COUNT: "+ str(favoCnt))
        break
