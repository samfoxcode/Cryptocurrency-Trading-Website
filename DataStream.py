from datetime import datetime, timedelta
from django.utils import timezone
import time
import threading
import json
import requests
import sys
import json
from django.utils import timezone
from home.models import Old_Prices, Coins, Tweets
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler 
from tweepy import Stream

access_token = ''
access_token_secret = ''
consumer_key = ''
consumer_secret = ''

def DataStream():
    while(True):
        #set the time to stream the data
        timeToRun = datetime.now() + timedelta(seconds=30)

        #Request data from coinmarketcap and parse the data
        r = requests.get('https://api.coinmarketcap.com/v1/ticker/')
        print("--------------------------------------------------------------------------------------------------------------------------")
        for coin in r.json():
            print(datetime.now(), coin["symbol"], coin["price_usd"],)
            if not Coins.objects.filter(ticker = coin["symbol"]).exists():
                web = "NO WEBSITE"
                if coin["symbol"] == "BTC":
                    web = "https://bitcoin.org"
                if coin["symbol"] == "XRP":
                    web = "https://ripple.com"
                if coin["symbol"] == "LTC":
                    web = "https://litecoin.org"
                if coin["symbol"] == "ETH":
                    web = "https://Ethereum.org"
                coinz = Coins(ticker = coin["symbol"], coin_name=coin["name"], website = web, current_price = coin["price_usd"], gain_loss = 0)
                coinz.save()
            else:
                coinz = Coins.objects.get(ticker= coin["symbol"])

            Price = Old_Prices(timestamp = timezone.now(), ticker = coinz, accuracy_projection = 0, price = coin["price_usd"])
            Price.save()

        # Wait until timeToRun has passed to fetch new data
        while(datetime.now() < timeToRun):
            time.sleep(1)

t1 = threading.Thread(target=DataStream)

def StartStream():
    # Create a thread to run the data stream
    t1.start()
    
#This is a basic listener that just prints received tweets to stdout.
class ToFileListener(StreamListener):
    def on_data(self, data):
        datajson = json.loads(data)
        print(datajson["text"]) #for visualization
        tweets = Tweets(ticker = "ETH", text=datajson["text"], sentiment = 0, current_price = 0, timestamp=timezone.localtime())
        tweets.save()

    def on_error(self, status):
        print(status)

def tweet_streaming():
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = ToFileListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #filter Twitter Streams to capture data by the keywords
    stream.filter(track=['ethereum'])#locations=[-80,40,-77,41.5])

t2 = threading.Thread(target=tweet_streaming)

def StartTwitterStream():
    t2.start()