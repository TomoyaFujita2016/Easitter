import sys
import twitterApiSetup

args = sys.argv
if len(args) > 1 :
    api = twitterApiSetup.tweetSetup()
    api.update_status(status=args[1])
