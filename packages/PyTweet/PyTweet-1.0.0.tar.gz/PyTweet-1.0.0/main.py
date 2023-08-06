import os
import random
from twitter import Client 

api_key = os.getenv("api_key")
api_key_secret = os.getenv("api_key_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("acces_token_secret")

client = Client(os.getenv("bearer_token"), consumer_key=api_key, consumer_key_secret=api_key_secret, access_token=access_token, access_token_secret=access_token_secret)
tweet=client.get_tweet(1420560381454426114) 
for user in [user.username for user in tweet.author.followers]:
    print(user)