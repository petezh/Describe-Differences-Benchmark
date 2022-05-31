import tweepy
import pandas as pd
from utils import encode_ascii

from parameters import *

CONSUMER_KEY = "jemyT8R4iNSnxfTzQle3yhKoR"
CONSUMER_SECRET = "I0UbgO3A3hRIyGiuwZqewwwKJ0wGTd6at3DN7UB8qJkjbD7518"
OAUTH_TOKEN = "721879494508879873-ClWBh6Jf4mrS0L1iWFgddFYfVgQXpTX"
OAUTH_TOKEN_SECRET = "DF8E3AGsQeArrSpdQUTh4auGM6ti9Knq9hR3xtrN2e5JZ"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def get_tweet_info(row):
    id_of_tweet = int(row['ID'])
    try:
        tweet = api.get_status(id_of_tweet)
        row['text'] = tweet.text
    except:
        row['text'] = None
    return row

def scrape():

    paths = {
        'all_lives_matter':f'{MANUAL_FOLDER}/blm_countermovements/AllLivesMatter_IDs.csv',
        'blue_lives_matter':f'{MANUAL_FOLDER}/blm_countermovements/BlueLivesMatter_IDs.csv',
        'white_lives_matter':f'{MANUAL_FOLDER}/blm_countermovements/WhiteLivesMatter_IDs.csv',
    }

    df = pd.DataFrame()
    for movement, filepath in paths.items():
        with open(filepath, 'r') as f:
            IDs = f.readlines()[1:]
            movement_df = pd.DataFrame({'movement':movement, 'ID':IDs}).sample(n=1000, replace=False, random_state=0)
            df = df.append(movement_df)

    df = df.apply(get_tweet_info, axis=1)
    df = df.dropna(axis=0)
    
    data = {}
    for movement in paths:
        data[movement] = df[df.movement==movement].text.apply(encode_ascii).tolist()
    
    return data