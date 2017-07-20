import tweepy
import twitterApiSetup as tas
import time
import random
api = tas.tweetSetup()
favoCnt = 0
errorCnt = 0
tags = ["#いいねした人全員フォローする"]
print("Let's Favorite !!")
while True:
    try:
        for tweet in api.search(q=tags, count=100):
            try:
                #api.create_favorite(tweet.id)
                tweet.favorite
                print("Successed in favoritting this tweet ! id: "+ str(tweet.id)+"\ntext:"+tweet.text)
                favoCnt += 1
                errorCnt = 0

            except tweepy.error.TweepError:
                    print("ERROR: FAILED TO FAVORITE!("+str(errorCnt)+") name:"+ tweet.user.name + " id:"+str(tweet.id))
                    errorCnt += 1
            except Exception:
                print("ERROR OCCUERD!!")
            if(((favoCnt != 0) and(favoCnt % 40 == 0)) or (errorCnt >= 10)):
                errorCnt = 0
                print("Zzzzzzzz.....")
                time.sleep(120)
            time.sleep(2 + random.randint(0,4))
            
    except KeyboardInterrupt:
        print("\nFAVO COUNT: "+ str(favoCnt))
        break
