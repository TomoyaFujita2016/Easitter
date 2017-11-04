# coding: utf-8
import tweepy
import pickle as pkl
import os

ACCESS_PATH = "./AC_PATH/accessCodes.pkl"

def encryptCode(code):
    return code.encode('utf8').encode('base64_codec').encode('rot_13')
def decryptCode(code):
    return code.decode('rot_13').decode('base64_codec').decode('utf8')

def tweetSetup():
    CONSUMER_KEY = 'DdaLMhxUN4fsPocqGVn2Dhya5'
    CONSUMER_SECRET = 'InmvzQj3b49SU9vqGyRgocwBrjLHwAuinzUsy0v2pz0JD96kuM'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    
    if not os.path.exists(ACCESS_PATH):
        redirect_url = auth.get_authorization_url()
        print ('Get your verification code from:' + redirect_url)
        verifier = input("Type the verification code: ").strip()
        auth.get_access_token(verifier)
        ACCESS_CODES = [auth.access_token]
        ACCESS_CODES.append(auth.access_token_secret)
        
        dirPath = os.path.dirname(ACCESS_PATH)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        with open(ACCESS_PATH,'wb') as f1:
            pkl.dump(ACCESS_CODES,f1)
    else:
        with open(ACCESS_PATH, 'rb') as f2:
            ACCESS_CODES = pkl.load(f2)

    auth.set_access_token(ACCESS_CODES[0], ACCESS_CODES[1])
    print ("DONE!")
    return tweepy.API(auth, api_root='/1.1', wait_on_rate_limit = True)
