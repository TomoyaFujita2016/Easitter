import tweepy
import pickle as pkl
import os

def savePklFile(path, data):
    dirPath = path.split("/")
    if 1 < len(dirPath):
        dirPath = "/".join(list(dirPath)[0:-1]) + "/"
        os.makedirs(dirPath, exist_ok=True)
    with open(path, "wb") as f:
        pkl.dump(data, f)

def readPklFile(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pkl.load(f)
    else:
        return []
        

def tweetSetup():
    CONSUMER_KEY = 'warrm7a0cjWy62GbnjQRLUXtd'
    CONSUMER_SECRET = '56CITHgkJyhx824WlYyM8lgp4sBE2M6j1bo4PfxXBY4Oti1Cz5'
    pklPath = "./.Data/pklData.pkl"
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    data = readPklFile(pklPath)
    if data == []:
        redirect_url = auth.get_authorization_url()
        print ('Get your verification code from:' + redirect_url)
        verifier = input("Type the verification code: ").strip()
        auth.get_access_token(verifier)
        ACCESS_TOKEN = auth.access_token
        ACCESS_SECRET = auth.access_token_secret
        data = [ACCESS_TOKEN, ACCESS_SECRET]
        savePklFile(pklPath, data)
    else:
        ACCESS_TOKEN = data[0]
        ACCESS_SECRET = data[1]
    
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    
    print ("DONE!")
    return tweepy.API(auth, api_root='/1.1', wait_on_rate_limit = True)
