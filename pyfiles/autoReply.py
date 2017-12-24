#coding: utf-8
import tweepy 
import time
import random
import os
from tqdm import tqdm
from datetime import datetime as dtdt
import datetime as dt



def main(easitter):
    print("MODE: auto reply")
    words = ["あり", "いいね"]
    cnt = 0
    try:
        timeline=easitter.getMention(befDays=-1)
        for status in timeline:
            print("[%3d]Reply: " % cnt)
            statusId=status.id
            screenName=status.author.screen_name
            message = "@"+ str(screenName) +" "+ createMessage()
            log = easitter.tweet(message, reply=statusId)
            print(log)
    except tweepy.error.TweepError as tp:
        print(tp)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass
    print("\nReplyCnt: %4d" % cnt)

def createMessage():
    message = [
            "(⦿＿⦿)",
            "^^",
            "(@o@ !!",
            "( ಠωಠ)",
            "‹‹\(´ω` )/››‹‹\( 　´)/››‹‹\( ´ω`)/››",
            "(*´∀｀*)ﾉ｡+ﾟ *｡",
            "Σ･∴=≡(っ'ヮ'c)ｳｩｯﾋｮｵｱｱｧ",
            "✌('ω'✌ )三✌('ω')✌三( ✌'ω')✌",
            "ヾ(⌒(ﾉ'ω')ﾉ",
            "ε=ヾ(*・∀・)/"
            ]
    num = random.randint(0, len(message)-1)
    return message[num]
