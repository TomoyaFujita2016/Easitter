#coding: utf-8
import tweepy
import twitterApiSetup as tas
import time
import os
import random
api = tas.tweetSetup()
#input own id to users
users = [883630081473617921];
byManyError = False
favoCnt = 0
errorCnt = 0
manyErrorCnt = 0
Cnt = 0

print("Let's flatter !!")
while True:
    try:
        for tweet in api.home_timeline(count=100):
            try:
                if 350 < favoCnt:
                    users = []
                tweetId = tweet.id
                tweetUser = tweet.user.id
                if tweetUser not in users:
                    api.create_favorite(tweetId)
                    print("Successed in flattering this tweet !("+str(favoCnt + 1) +") id: "+ str(tweetId))
                    users.append(tweetUser)
                    favoCnt += 1
                else:
                    print("Already flattered: " + str(tweetUser))
                
                errorCnt = 0
                manyErrorCnt = 0

            except tweepy.error.TweepError as terr:
                print("ERROR: FAILED TO FLATTER!("+str(errorCnt)+") name:"+ tweet.user.name + " id:"+str(tweet.id))
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
                time.sleep(90)
                byFirst = True
            Cnt += 1
            if(byManyError):
                byManyError = False
                manyErrorCnt += 1
                print("ManyError: back to start tweet")
                break
            if(manyErrorCnt >= 2):
                print("TOO MANY ERRORS !!")
                print("Flattering is done !")
                os.system('date')
                raise KeyboardInterrupt
            time.sleep(1 + random.randint(0,1))

            
            
    except KeyboardInterrupt:
        print("\nFLATTERING COUNT: "+ str(favoCnt))
        break
