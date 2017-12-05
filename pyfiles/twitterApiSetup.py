# coding: utf-8
import tweepy
import pickle as pkl
import os

ACCESS_PATH = "AC_PATH/accessCodes.pkl"

def encryptCode(code):
    return code.encode('utf8').encode('base64_codec').encode('rot_13')
def decryptCode(code):
    return code.decode('rot_13').decode('base64_codec').decode('utf8')

def getAccessKeys():
    CK = "OMTYKPcmnzPetbhRphClw7obj"
    CS = "rD9f14DfDKrJyVg2LcvUBRphSLi0afxjpP6o63Pe6AFCV0xnUH"
    ACCESS_CODES = [CK, CS]
    auth = tweepy.OAuthHandler(CK, CS)
    
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

    return ACCESS_CODES
