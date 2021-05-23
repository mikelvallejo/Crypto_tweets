# Extract Data from Coinbase API

from Historic_Crypto import HistoricalData
df= HistoricalData('BTC-USD',86400,'2021-01-01-00-00').retrieve_data()

from Historic_Crypto import HistoricalData
df_eth= HistoricalData('ETH-USD',86400,'2021-01-01-00-00').retrieve_data()

# Extract Data from Twitter API
import tweepy
import csv

consumer_key='XXXXX'
consumer_secret='XXXXX'
access_key='XXXXX'
access_secret='XXXXX'

def get_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    #read csv
    with open('/Users/mikel/Documents/Projects/Crypto_tweets/elonmusk_tweets.csv', 'r') as elonmusk:
        elon_tweets=list(csv.reader(elonmusk))
    
    alltweets=[]
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print(f"...{len(alltweets)} tweets downloaded so far")
    
    #transform the tweepy tweets into a 2D array that will populate the csv 
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    elon_tweets+=outtweets
    
    #write the csv  
    with open('/Users/mikel/Documents/Projects/Crypto_tweets/elonmusk_tweets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(elon_tweets)
    pass
    
#Select the tweets that contain crypto topics givin boolean value True/False.
crypto_topics_lst = ['bitcoin', 'Bitcoin', 'crypto', 'Crypto', 'Blockchain', 
                     'blockchain', 'Regulation', 'Doge', 'doge', 'DOGE', 'Ethereum', 
                     'ethereum', 'Money', 'money', 'Currency', 'currency', 
                    'Coin', 'coin', 'DeFi', 'ETF', 'BTC']

new_lst=[]
        
for i in df_elon['text']:
    new_lst.append(any(ele in i for ele in crypto_topics_lst))

#Transform that list into a new column
df_elon['boolean']=new_lst

#Do not take mentions
df_elon_true= df_elon_true[~df_elon_true['Tweet'].astype(str).str.startswith('@')]