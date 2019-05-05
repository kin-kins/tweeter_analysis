
# coding: utf-8

# In[1]:


import tweepy
import pandas as pd
import numpy as np
import json
import datetime as dt
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


# In[2]:

def twitter_setup():

    CONSUMER_KEY    = ''
    CONSUMER_SECRET = ''

    # Access:
    ACCESS_TOKEN  = ''
    ACCESS_SECRET = ''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


    api = tweepy.API(auth,wait_on_rate_limit=True,
                    wait_on_rate_limit_notify=True)
    return api


# In[3]:


def auth():
    twitterObj = twitter_setup()
    if (not twitterObj):
        return("Authentication Problem")
    else:
        return ("Authenticated")


# In[4]:


def follower(userName):
    twitterObj = twitter_setup()
    followers=[]
    followers= twitterObj.followers(userName,-1)
    #print(followers)
    follData= pd.DataFrame()
    follData['id']=np.array([User.id for User in followers])
    follData['user']=np.array([User.screen_name for User in followers])
    follData['location']=np.array([User.location for User in followers])
    #follData['name']= np.array(tweet.name for tweet in followers)
    return(follData.head(100))



# In[49]:


def alltweet():
    twitterObj = twitter_setup()
    allTweets=twitterObj.user_timeline(id='ashu__kumar',count=200)
    data = pd.DataFrame()
    data = pd.DataFrame(data=[tweet.text for tweet in allTweets], columns=['Tweets'])
    data['len']  = np.array([len(tweet.text) for tweet in allTweets])
    data['ID']   = np.array([tweet.id for tweet in allTweets])
    data['Date'] = np.array([tweet.created_at for tweet in allTweets])
    data['Source'] = np.array([tweet.source for tweet in allTweets])
    data['Likes']  = np.array([tweet.favorite_count for tweet in allTweets])
    data['RTs']    = np.array([tweet.retweet_count for tweet in allTweets])
    data['Location'] = np.array([tweet.geo for tweet in allTweets])
    #print(data['Date'])
    return(data)


localData=alltweet()



#         countYearTweet=[]
#         countYearMonth=[]
#         countYearDay=[]
#         for x in pd_year:
#             if(x==curYear):
#                 countYearTweet+=[count]
#             elif ((x==curYear-1)and(pd_month[count]>curMonth)):
#                 countYearTweet+=[count]
#             elif ((x==curYear-1)and(pd_month[count]==curMonth)and(pd_day[count]>=curDay)):
#                 countYearTweet+=[count]
#             if(x==curYear)and(pd_month[count]==curMonth):
#                 countYearMonth+=[count]
#             if(x==curYear)and(pd_month[count]==curMonth)and(pd_day[count]==curDay):
#                 countYearDay+=[count]
#             count+=1
#         print (len(countYearMonth))
#         for x in countYearMonth:
#             print (data.at[x,'Tweets'])








# In[ ]:


def timeAnalysis(curYear):
    data=localData
    pd_year=pd.DatetimeIndex(data['Date']).year
    pd_month=pd.DatetimeIndex(data['Date']).month
    pd_day=pd.DatetimeIndex(data['Date']).day
    today=dt.datetime.now()
    curDay=today.day
    curMonth=today.month
    #curYear=today.year
    #print(pd_month[0])
    count=0;
    #count_month={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}
    count_month=[0,0,0,0,0,0,0,0,0,0,0,0]

    for y in range(1,13):
        count=0
        for x in pd_year:
            if(x==curYear)and(pd_month[count]==y):
                    count_month[y]+=1
            count+=1

    return(count_month)


# In[ ]:
def pdYear():
       data=localData
       pd_year=pd.DatetimeIndex(data['Date']).year
       print (pd_year.unique)
       return (pd_year)

def minYear():
       data=localData
       pd_year=pd.DatetimeIndex(data['Date']).year
       return min(pd_year)


# In[ ]:


def maxYear():
       data=localData
       pd_year=pd.DatetimeIndex(data['Date']).year
       return max(pd_year)

def validUser(userName):
    twitterObj = twitter_setup()
    try:
        user=twitterObj.get_user(userName)
    except tweepy.TweepError as e:
        print (e.api_code)
        return "Invalid User"
    return "Valid User"



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H1(
        children='Tweeter Analysis DashBoard',
        style={
            'textAlign': 'center',
            'color': 'orange'
        }
    ),
    html.H6(
                children='Enter UserName',
                style={
                    'textAlign': 'left',
                    'color':'blue'
                }
            ),

    dcc.Input(
        id='user',
        type='text',
        value='user'
    ),
    html.Div(id='valid_user'),
         dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in ['tweets','likes','retweets']],
                value='tweets'
            ),

    dcc.Graph(id='graphe'),
    dcc.Slider(
        id='year-slider',
        min=minYear(),
        max=maxYear(),
        value=maxYear(),
        marks={str(year): str(year) for year in pdYear().unique()},
        step=None
    )

])


# In[9]:


@app.callback(
    Output('valid_user', 'children'),
    [Input('user', 'value')]
)
def callback_a(x):
    return validUser(x)

@app.callback(
    Output('graphe', 'figure'),
    [Input('year-slider', 'value')]
)
def callback_a(slider_year):
    trace1 = go.Bar(
    x=[1,2,3,4,5,6,7,8,9,10,11,12],
    y=timeAnalysis(slider_year),
    name='Tweets'
)
    return {'data': [trace1],
    'layout':
    go.Layout(
        title='Tweet count'
        )
    }



if __name__ == '__main__':
    app.run_server(debug=True)
