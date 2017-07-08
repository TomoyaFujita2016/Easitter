import twitterApiSetup as setup

api = setup.tweetSetup()

result = api.search(q="#絵描きさんと繋がりたい")

for res in result:
    print(res.text)
