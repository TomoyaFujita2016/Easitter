# coding: utf-8
import tweepy
import pickle as pkl
import os
import random
import shutil as sh

ACCESS_PATH = "AC_PATH/accessCodes.pkl"
C_PATH = ".CSCK.txt"
NUM_PATH  = ".number.pkl"
FIRST_PATH = ".byFirst"

def initialize():
    if byFirstExecution():
        if os.path.exists(ACCESS_PATH):
            os.remove(ACCESS_PATH)
        if os.path.exists(NUM_PATH):
            os.remove(NUM_PATH)

def encryptCode(code):
    return code.encode('utf8').encode('base64_codec').encode('rot_13')
def decryptCode(code):
    return code.decode('rot_13').decode('base64_codec').decode('utf8')

def getCs():
    CS = []
    with open(C_PATH, "r") as f:
        for line in f:
            CS.append(line.replace("\n", ""))
    return CS

def byFirstExecution():
    if os.path.exists(FIRST_PATH):
        os.remove(FIRST_PATH)
        return True
    return False

def selectCS():
    CS = getCs()
    if os.path.exists(NUM_PATH):
        with open(NUM_PATH, "rb") as f:
            rand = pkl.load(f)
            print("CSCK: " + str(rand))
        return CS[rand].split(",")
    
    rand = random.randint(0, len(CS)-1)
    print("CSCK: " + str(rand))
    with open(NUM_PATH, "wb") as f:
        pkl.dump(rand, f)
    return CS[rand].split(",")
        

def tweetSetup():
    initialize()
    ACCESS_CODES = selectCS()
    auth = tweepy.OAuthHandler(ACCESS_CODES[0], ACCESS_CODES[1])
    print("auth done") 
    if not os.path.exists(ACCESS_PATH):
        redirect_url = auth.get_authorization_url()
        print ('Get your verification code from:' + redirect_url)
        verifier = input("Type the verification code: ").strip()
        auth.get_access_token(verifier)
        ACCESS_CODES.append(auth.access_token)
        ACCESS_CODES.append(auth.access_token_secret)
        
        dirPath = os.path.dirname(ACCESS_PATH)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        with open(ACCESS_PATH,'wb') as f1:
            pkl.dump(ACCESS_CODES,f1)
    else:
        with open(ACCESS_PATH, 'rb') as f2:
            ACCESS_CODES = pkl.load(f2)

    auth = tweepy.OAuthHandler(ACCESS_CODES[0], ACCESS_CODES[1])
    auth.set_access_token(ACCESS_CODES[2], ACCESS_CODES[3])

    return tweepy.API(auth, api_root='/1.1', wait_on_rate_limit = True)
