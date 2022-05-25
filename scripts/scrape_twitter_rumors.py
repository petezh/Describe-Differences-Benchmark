import tweepy
import pandas as pd

CONSUMER_KEY = "jemyT8R4iNSnxfTzQle3yhKoR"
CONSUMER_SECRET = "I0UbgO3A3hRIyGiuwZqewwwKJ0wGTd6at3DN7UB8qJkjbD7518"
OAUTH_TOKEN = "721879494508879873-ClWBh6Jf4mrS0L1iWFgddFYfVgQXpTX"
OAUTH_TOKEN_SECRET = "DF8E3AGsQeArrSpdQUTh4auGM6ti9Knq9hR3xtrN2e5JZ"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def get_tweet_info(row):
    id_of_tweet = int(row['Tweet ID'])
    try:
        tweet = api.get_status(id_of_tweet)
        row['text'] = tweet.text
        row['dt'] = tweet.created_at
    except:
        row['text'] = None
        row['dt'] = None
    return row

STAGES = ['early', 'mid', 'late']

def scrape():

    URLS = {
        'redhawks':'https://zenodo.org/record/2563864/files/DATASET_R1.xlsx',
        'muslim_waitress':'https://zenodo.org/record/2563864/files/DATASET_R2.xlsx',
        'zuckerberg_yatch':'https://zenodo.org/record/2563864/files/DATASET_R3.xlsx',
        'denzel_washington':'https://zenodo.org/record/2563864/files/DATASET_R4.xlsx',
        'veggietales':'https://zenodo.org/record/2563864/files/DATASET_R7.xlsx',
        'michael_jordan':'https://zenodo.org/record/2563864/files/DATASET_R2.xlsx',
    }

    data = {}

    for rumor, url in URLS.items():

        print(rumor)

        df = pd.read_excel(url)
        df = df.sample(300)
        df = df.apply(get_tweet_info, axis=1)
        df = df.dropna(axis=0)
        df['stage'] = pd.qcut(df['dt'], 3, labels=STAGES)

        for stage in STAGES:
            data[f'{rumor}_{stage}'] = df[df.stage == stage]['text'].tolist()
    
    return data