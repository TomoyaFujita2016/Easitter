import tweepy
def tweetSetup():
    CONSUMER_KEY = 'DdaLMhxUN4fsPocqGVn2Dhya5'
    CONSUMER_SECRET = 'InmvzQj3b49SU9vqGyRgocwBrjLHwAuinzUsy0v2pz0JD96kuM'
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
