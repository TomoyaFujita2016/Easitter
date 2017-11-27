#coding: utf-8
import tweepy
from pyfiles import twitterApiSetup as tas
import requests
import time
import shutil
import pickle as pkl
import os
import sys
import traceback

def confirmPklFile(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pkl.load(f)
    else:
        return []

def download_img(url, file_name, downloadCnt, SAVE_DIR):
    print("[%4d]Downloading from "%downloadCnt + url)
    r = requests.get(url+":orig", stream=True)
    if r.status_code == 200:
        with open(SAVE_DIR + file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def savePklFile(path, data):
    with open(path, "wb") as f:
        pkl.dump(data, f)

def newTweetId(api, tag):
    tweetData = api.search(q=tag, count=1)
    if len(tweetData) == 0:
        return 0
    return tweetData[-1].id

def main():
    PKL_DIR = "./PklData/"
    TWEET_IDS_PATH = "TWEET_IDS.pkl"
    IMAGE_URLS_PATH = "IMAGE_URLS_PATH.pkl"
    SAVE_DIR = "./ImagesFromTwitter/"
    TAGS = ["shose", "eee"]
    downloadCnt = 0
    NUMBER_OF_GET = 20
    try: 
         if not os.path.exists(SAVE_DIR):
             os.mkdir(SAVE_DIR)
         if not os.path.exists(PKL_DIR):
             os.mkdir(PKL_DIR)

         tweetIDs = confirmPklFile(PKL_DIR + TWEET_IDS_PATH)
         imageUrls = confirmPklFile(PKL_DIR + IMAGE_URLS_PATH)
         
         api = tas.tweetSetup()
         for tag in TAGS:
             print("TAG: " + tag)
             maxId = newTweetId(api, tag)
             if maxId == 0:
                 print("No result!")
                 continue
             for ep in range(NUMBER_OF_GET):
                 try:
                     print("PAGE: " + str(ep))
                     print("TweetId: ~" + str(maxId))
                     # print("max"+str(maxId))
                     tweets = api.search(q=tag, count=100, max_id=maxId-1) 
                     if len(tweets) == 0:
                         print("Already taken all images within 1 week.")
                         break
                     maxId = tweets[-1].id
                     for tweet in tweets:
                         if not hasattr(tweet, "extended_entities"):
                             # print("extended_entities is not included !")
                             continue
                         if not(tweet.id in tweetIDs) and ("media" in tweet.extended_entities):
                             for media in tweet.extended_entities['media']:
                                 url = media["media_url_https"]
                                 if not url in imageUrls:
                                    downloadCnt += 1
                                    download_img(url, url.split("/")[-1], downloadCnt, SAVE_DIR)
                                    imageUrls.append(url)
                             tweetIDs.append(tweet.id)
                 except tweepy.error.TweepError as terr:
                     print(terr)
                 time.sleep(1)
                         
         
         savePklFile(PKL_DIR + TWEET_IDS_PATH, tweetIDs)
         savePklFile(PKL_DIR + IMAGE_URLS_PATH, imageUrls)
         print("\n"+str(downloadCnt) + " images is downloaded !")
    except:
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
