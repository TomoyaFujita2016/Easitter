if main(easitter):
    tag = ["Tensorflow", "Keras", "Chainer"]
    tweets = easitter.searchTweets(tag, tweetNum=10, resultType="popular")
