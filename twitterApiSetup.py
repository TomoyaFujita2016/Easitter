import tweepy
def tweetSetup():
    CONSUMER_KEY = 'Yf4SVt0IhyEQCPxMz8ShEXDng'
    CONSUMER_SECRET = '4aH1lnFk8FlEUL3qkZzV7p64qdzRq41OZRaeLTp1aPvoaJbHvg'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    
    redirect_url = auth.get_authorization_url()
    print ('Get your verification code from:' + redirect_url)
    verifier = input("Type the verification code: ").strip()
    auth.get_access_token(verifier)
    ACCESS_TOKEN = auth.access_token
    ACCESS_SECRET = auth.access_token_secret
    
    
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    
    print ("DONE!")
    return tweepy.API(auth, api_root='/1.1', wait_on_rate_limit = True)
