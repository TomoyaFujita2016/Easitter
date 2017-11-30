from pyfiles import twitterApiSetup as tas
from pyfiles import byFaceDetection as byF
import requests
import time
from tqdm import tqdm
import shutil
import pickle as pkl
import os
import sys
import traceback
import cv2

def confirmPklFile(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pkl.load(f)
    else:
        return []

def download_img(url, file_name, downloadCnt, SAVE_DIR, SAVE_DIR_FACE, byFace):
    # print("[%4d]Downloading from "%downloadCnt + url)
    r = requests.get(url+":orig", stream=True)
    if r.status_code == 200:
        with open(SAVE_DIR + file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        if byFace:
            image = cv2.imread(SAVE_DIR + file_name)
            exFace = byF.detectFace(image)
            if exFace:
                cv2.imwrite(SAVE_DIR_FACE + file_name, image)

def savePklFile(path, data):
    with open(path, "wb") as f:
        pkl.dump(data, f)

def newTweetId(api, tag):
    tweetData = api.search(q=tag, count=1)
    if len(tweetData) == 0:
        return 0
    return tweetData[-1].id

def main(TAGS = ["クラフトビール"], byFACE=False):
    green = "\033[34m"
    cyan = "\033[36m"
    blue = "\033[35m"
    end = "\033[0m"
    PKL_DIR = "./PklData/"
    TWEET_IDS_PATH = "TWEET_IDS.pkl"
    IMAGE_URLS_PATH = "IMAGE_URLS_PATH.pkl"
    SAVE_DIR = "./ImagesFromTwitter/"
    SAVE_DIR_FACE = "./ImageFromTwitterFace/"
    downloadCnt = 0
    NUMBER_OF_GET = 100
    try: 
         if not os.path.exists(SAVE_DIR):
             os.mkdir(SAVE_DIR)
         if not os.path.exists(PKL_DIR):
             os.mkdir(PKL_DIR)
         if not os.path.exists(SAVE_DIR_FACE) and byFACE:
             os.mkdir(SAVE_DIR_FACE)

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
                     print(blue + "PAGE: " + str(ep))
                     print("TweetId: ~" + str(maxId) + green)
                     # print("max"+str(maxId))
                     tweets = api.search(q=tag, count=100, max_id=maxId-1) 
                     if len(tweets) == 0:
                         print("Already taken all images within 1 week.")
                         break
                     maxId = tweets[-1].id
                     pBar = tqdm(tweets)
                     oldI = 0
                     for i, tweet in enumerate(pBar):
                         if not hasattr(tweet, "extended_entities"):
                             # print("extended_entities is not included !")
                             continue
                         if not(tweet.id in tweetIDs) and ("media" in tweet.extended_entities):
                             for media in tweet.extended_entities['media']:
                                 url = media["media_url_https"]
                                 if not url in imageUrls:
                                    downloadCnt += 1
                                    pBar.set_description("[%4d]"%downloadCnt+cyan+"Downloading from ..%s" % url[28:44]+".." + green)
                                    download_img(url, url.split("/")[-1], downloadCnt, SAVE_DIR, SAVE_DIR_FACE, byFACE)
                                    imageUrls.append(url)
                             tweetIDs.append(tweet.id)
                         pBar.update(i - oldI)
                         oldI = i
                 except:
                     _, _, tb = sys.exc_info()
                     traceback.print_tb(tb)
                 time.sleep(1)
         
         savePklFile(PKL_DIR + TWEET_IDS_PATH, tweetIDs)
         savePklFile(PKL_DIR + IMAGE_URLS_PATH, imageUrls)
         print("\n"+end+str(downloadCnt) + " images is downloaded !")
    except:
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
