from pyfiles import byFaceDetection as byF
import requests
import time
from tqdm import tqdm
import shutil
import pickle as pkl
import os
import sys

byCv = True
try:
    import cv2
except:
    byCv = False

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

def main(easitter, TAGS = ["クラフトビール"], byFACE=False):
    PKL_DIR = "./PklData/"
    TWEET_IDS_PATH = "TWEET_IDS.pkl"
    IMAGE_URLS_PATH = "IMAGE_URLS_PATH.pkl"
    SAVE_DIR = "./ImagesFromTwitter/"
    SAVE_DIR_FACE = "./FaceImageFromTwitter/"
    downloadCnt = 0
    NUMBER_OF_GET = 5000
    users = set()

    if byFACE:
        byFACE = byCv

    if not os.path.exists(SAVE_DIR):
        os.mkdir(SAVE_DIR)
    if not os.path.exists(PKL_DIR):
        os.mkdir(PKL_DIR)
    if not os.path.exists(SAVE_DIR_FACE) and byFACE:
        os.mkdir(SAVE_DIR_FACE)

    tweetIDs = confirmPklFile(PKL_DIR + TWEET_IDS_PATH)
    imageUrls = confirmPklFile(PKL_DIR + IMAGE_URLS_PATH)

    for tag in TAGS:
        print("TAG: %s" % tag)
        tweets = easitter.searchTweets(tag, limit=NUMBER_OF_GET)
        filteredTweets, users = easitter.tweetsFiltering(tweets, users=users)
        
        for tweet in filteredTweets:
            if not hasattr(tweet, "extended_entities"):
                continue
            if not(tweet.id in tweetIDs) and ("media" in tweet.extended_entities):
                for media in tweet.extended_entities['media']:
                    url = media["media_url_https"]
                    if not url in imageUrls:
                        downloadCnt += 1
                        print("[%4d]"%downloadCnt+"Downloading from %s" % url)
                        download_img(url, url.split("/")[-1], downloadCnt, SAVE_DIR, SAVE_DIR_FACE, byFACE)
                        imageUrls.append(url)
                    tweetIDs.append(tweet.id)

    savePklFile(PKL_DIR + TWEET_IDS_PATH, tweetIDs)
    savePklFile(PKL_DIR + IMAGE_URLS_PATH, imageUrls)
    print("\n" + str(downloadCnt) + " images is downloaded !")
