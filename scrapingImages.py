#coding: utf-8
import tweepy
import twitterApiSetup as tas
import requests
import shutil
import pickle as pkl
import os

PKL_DIR = "Data/"
TWEET_IDS_PATH = "TWEET_IDS.pkl"
IMAGE_URLS_PATH = "IMAGE_URLS_PATH.pkl"
SAVE_DIR = "ImagesFromTwitter/"
TAGS = ["写真"]

def confirmPklFile(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pkl.load(f)
    else:
        return []

def download_img(url, file_name):
    print("Downloading from " + url)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(SAVE_DIR + file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def savePklFile(path, data):
    with open(path, "wb") as f:
        pkl.dump(data, f)

if __name__=='__main__':
    if not os.path.exists(SAVE_DIR.split("/")[0]):
        os.mkdir(SAVE_DIR.split("/")[0])
    if not os.path.exists(PKL_DIR.split("/")[0]):
        os.mkdir(PKL_DIR.split("/")[0])

    tweetIDs = confirmPklFile(PKL_DIR + TWEET_IDS_PATH)
    imageUrls = confirmPklFile(PKL_DIR + IMAGE_URLS_PATH)
    
    api = tas.tweetSetup()
    
    while True:
        try:
            for tag in TAGS:
                for tweet in api.search(q=TAGS, count=1000):
                    if not hasattr(tweet, "extended_entities"):
                        # print("extended_entities is not included !")
                        continue
                    if (not tweet.id in tweetIDs) and ("media" in tweet.extended_entities):
                        for media in tweet.extended_entities['media']:
                            url = media["media_url_https"]
                            download_img(url, url.split("/")[-1])
                            imageUrls.append(url)
                            tweetIDs.append(tweet.id)
        except KeyboardInterrupt:
            break
    
    savePklFile(PKL_DIR + TWEET_IDS_PATH, tweetIDs)
    savePklFile(PKL_DIR + IMAGE_URLS_PATH, imageUrls)
