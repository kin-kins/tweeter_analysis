import tweepy
import pandas as pd
import numpy as np
import json
import datetime as dt
import matplotlib.pyplot as plt
CONSUMER_KEY    = ''
CONSUMER_SECRET = ''

# Access:
ACCESS_TOKEN  = ''
ACCESS_SECRET = ''
def twitter_setup():

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


    api = tweepy.API(auth,wait_on_rate_limit=True,
                    wait_on_rate_limit_notify=True)
    return api
    
twitterObj = twitter_setup()
if (not twitterObj):
    print("Authentication Problem")
else:
    print ("Authenticated")
    user=[]
user = twitterObj.get_user('arkodyutisaha')
if(user):
    print((user))
else:
    print("user not found")
    
        allTweets=twitterObj.user_timeline(id="arkodyutisaha",count=500)
#         print (allTweets)
        data = pd.DataFrame()  
        data = pd.DataFrame(data=[tweet.text for tweet in allTweets], columns=['Tweets'])
        data['len']  = np.array([len(tweet.text) for tweet in allTweets])
        data['ID']   = np.array([tweet.id for tweet in allTweets])
        data['Date'] = np.array([tweet.created_at for tweet in allTweets])
        data['Source'] = np.array([tweet.source for tweet in allTweets])
        data['Likes']  = np.array([tweet.favorite_count for tweet in allTweets])
        data['RTs']    = np.array([tweet.retweet_count for tweet in allTweets])
        data['Location'] = np.array([tweet.geo for tweet in allTweets])
        print(data.head)
        x=(data['RTs']).idxmax()
print (x)
print(data.at[x,'Tweets'])
print(max(data['RTs']))
