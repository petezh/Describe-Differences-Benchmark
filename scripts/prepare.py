from collections import defaultdict
from io import BytesIO
import itertools
import json
import os
from os.path import join
import re
import requests
from typing import Dict

import gdown
import glob
import numpy as np
import pandas as pd
import shutil
from tqdm import tqdm
import tarfile
import zipfile

DOWNLOAD_FOLDER = 'source'
MANUAL_FOLDER = 'manual'
OUTPUT_FOLDER = 'output'

"""
**********
Preparers
**********
"""

def prepare_open_deception():
    """
    Downloads and formats the Open Deception dataset.
    """
    
    NAME = 'open_deception'
    TYPE = 'correlation'
    DESC = 'Arbitrary lies and truths from any domain generated by crowdsources.'
    URL = 'http://web.eecs.umich.edu/~mihalcea/downloads/openDeception.2015.tar.gz'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_tar(URL, directory)
    
    input_file = f'{directory}/OpenDeception/7Truth7LiesDataset.csv'
    df = pd.read_csv(input_file, quotechar="'", escapechar="\\")
    
    data = {
        'lie':df[df['class']=='lie']['text'].tolist(),
        'truth': df[df['class']=='truth']['text'].tolist()
    }
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_fake_news():
    """
    Downloads and formats the Fake News dataset.
    """
    
    NAME = 'fake_news'
    TYPE = 'correlation'
    DESC = 'A dataset of fake and legitimate news, covering several domains (technology, education, business, sports, politics, entertainment and celebrity news).'
    URL = 'http://web.eecs.umich.edu/~mihalcea/downloads/fakeNewsDatasets.zip'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_zip(URL, directory)

    files = glob.glob(f'{directory}/fakeNewsDatasets/fakeNewsDataset/**/*.txt')
    legit, fake = [], []
    for file in files:
        with open(file, 'r') as f:
            contents = f.read()
            if 'legit' in file:
                legit.append(contents)
            else:
                fake.append(contents)
    
    data = {
        'legit':legit,
        'fake':fake
    }

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_trial_deception():
    """
    Downloads and formats the Real-life Deception dataset.
    """

    NAME = 'trial_deception'
    TYPE = 'correlation'
    DESC = 'A multimodal dataset consisting of real-life deception: deceptive and truthful trial testimonies, manually transcribed and annotated.'
    URL = 'http://web.eecs.umich.edu/~mihalcea/downloads/RealLifeDeceptionDetection.2016.zip'
    
    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_zip(URL, directory)

    files = glob.glob(f'{directory}/Real-life_Deception_Detection_2016/Transcription/**/*.txt')
    truth, lie = [], []
    for file in files:
        with open(file, 'r') as f:
            contents = f.read()
            if 'truth' in file:
                truth.append(contents)
            else:
                lie.append(contents)
    
    data = {
        'truth':truth,
        'lie':lie
    }

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_rate_my_prof():
    """
    Downloads and formats Rate My Professor dataset.
    """

    NAME = 'rate_my_prof'
    TYPE = 'correlation'
    DESC = 'A dataset scraped from RateMyProfessor.com for professors\' teaching evaluation.'
    URL = 'https://md-datasets-cache-zipfiles-prod.s3.eu-west-1.amazonaws.com/fvtfjyvw7d-2.zip'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_zip(URL, directory)
    
    import gender_guesser.detector as gender

    d = gender.Detector()
    get_gender = lambda name: d.get_gender(name)

    df = pd.read_csv(join(directory, 'RateMyProfessor_Sample data.csv'))
    df['first_name'] = df['professor_name'].str.split().str[0]
    df['gender'] = df['first_name'].apply(get_gender)
    df['gender'].value_counts()

    df = df.sample(frac=1, random_state = 0)

    data = {
        'female':list(map(str, df[df['gender']=='female']['comments'])),
        'male':list(map(str, df[df['gender']=='male']['comments']))
    }

    data['female'] = [t for t in data['female'] if ' him ' not in t and ' his ' not in t]
    data['male'] = [t for t in data['male'] if ' she ' not in t and ' her ' not in t]

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_parenting_subreddits():
    """
    Downloads and formats parenting discussion threads on Reddit.
    """

    NAME = 'parenting_subreddits'
    TYPE = 'correlation'
    DESC = 'A dataset scraped from various parenting-related subreddits.'
    URL = 'https://raw.githubusercontent.com/GT-SALT/Parenting_OnlineUsage/main/data/0527_reddit_1300_parenting_clean.csv'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.csv'
    download_file(URL, directory, filename)
    
    df = pd.read_csv(join(directory, filename))
    df.head()

    df = df.dropna()
    topics = set(itertools.chain.from_iterable(df['topics'].str.split(',')))
    data = {}
    for topic in topics:
        text = df[df['topics'].str.contains(topic)]['text']
        clean_text = text.apply(lambda s: s.replace(u"\u2018", "'").replace(u"\u2019", "'"))
        data[topic] = clean_text.tolist()

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_diplomacy_deception():
    """
    Downloads and formats deception data from rounds of the game, Diplomacy.
    """

    NAME = 'diplomacy_deception'
    TYPE = 'correlation'
    DESC = 'Dataset contains diaglogue from a game of diplomacy labeled for deceptiveness.'
    URLS = {'test':'https://raw.githubusercontent.com/DenisPeskov/2020_acl_diplomacy/master/data/test.jsonl',
            'train':'https://raw.githubusercontent.com/DenisPeskov/2020_acl_diplomacy/master/data/train.jsonl',
            'validation':'https://raw.githubusercontent.com/DenisPeskov/2020_acl_diplomacy/master/data/validation.jsonl'}

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    for dataset, url in URLS.items():
        filename = f'{dataset}.txt'
        download_file(url, directory, filename)
    
    files = glob.glob(f'{directory}/*.txt')
    data = defaultdict(list)

    for file in files:
        df = pd.read_json(file, lines=True)
        messages = list(itertools.chain.from_iterable(pd.read_json(files[0], lines=True)['messages']))
        labels = list(itertools.chain.from_iterable(pd.read_json(files[0], lines=True)['sender_labels']))
        df = pd.DataFrame({'message':messages, 'label':labels})
        data['truth'].extend(df[df['label']==True]['message'].apply(lambda s: s.replace(u"\u2018", "'").replace(u"\u2019", "'")).tolist())
        data['lie'].extend(df[df['label']==False]['message'].apply(lambda s: s.replace(u"\u2018", "'").replace(u"\u2019", "'")).tolist())
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_abc_headlines():
    """
    Downloads and formats a million headlines from ABC news.
    """

    NAME = 'abc_headlines'
    TYPE = 'correlation'
    DESC = 'Dataset contains headlines from ABC news from 2003 to 2020.'
    URL = 'https://dataverse.harvard.edu/api/access/datafile/4460084'
    
    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.csv'
    download_file(URL, directory, filename)
    
    df = pd.read_csv(join(directory, filename), sep='\t')
    df['year'] = df['publish_date'].astype(str).str[:4].astype(int)
    
    data = {}
    for year in df['year'].unique():
        data[str(year)] = df[df['year']==year]['headline_text'].tolist()[:1000]
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_times_india_headlines():
    """
    Downloads and formats a million headlines from Times of India news.
    """

    NAME = 'times_india_headlines'
    TYPE = 'correlation'
    DESC = 'Dataset contains headlines across time from Times of India news from 2001 to 2022.'
    URL = 'https://dataverse.harvard.edu/api/access/datafile/6175512'
    
    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.csv'
    download_file(URL, directory, filename)
    
    df = pd.read_csv(join(directory, filename))
    df['year'] = df['publish_date'].astype(str).str[:4].astype(int)
    
    data = {}
    for year in df['year'].unique():
        data[str(year)] = df[df['year']==year]['headline_text'].tolist()[:1000]
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_clickbait_headlines():
    """
    Downloads and formats a million headlines from The Examiner, a clickbait news site.
    """

    NAME = 'clickbait_headlines'
    TYPE = 'correlation'
    DESC = 'Dataset contains headlines across time from the Examiner, a clickbait news site.'
    URL = 'https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/BFAZHR/WYSGGQ'
    
    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.csv'
    download_file(URL, directory, filename)
    
    df = pd.read_csv(join(directory, filename))
    df['year'] = df['publish_date'].astype(str).str[:4].astype(int)
    
    data = {}
    for year in df['year'].unique():
        data[str(year)] = df[df['year']==year]['headline_text'].tolist()[:1000]
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_stock_news():
    """
    Downloads and formats a million headlines from The Examiner, a clickbait news site.
    """

    NAME = 'stock_news'
    TYPE = 'causation'
    DESC = 'Dataset contains stock movement from Yahoo Finance paired with top headlines in Reddit.'
    URL = 'https://raw.githubusercontent.com/ShravanChintha/Stock-Market-prediction-using-daily-news-headlines/master/Combined_News_DJIA.csv'
    
    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.csv'
    download_file(URL, directory, filename)

    df = pd.read_csv(join(directory, filename))

    data = defaultdict(list)
    for col in df.columns:
        if "Top" in col:
            data['down'].extend(df[df['Label'] == 0][col].tolist())
            data['up'].extend(df[df['Label'] == 1][col].tolist())

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_unhealthy_conversations():
    """
    Downloads and formats data on unhealthy conversations.
    """

    NAME = 'unhealthy_conversations'
    TYPE = 'correlation'
    DESC = 'Dataset includes expert-annotated unhealthy conversations.'
    URLS = {'test':'https://raw.githubusercontent.com/conversationai/unhealthy-conversations/main/corpus/test.csv',
            'train':'https://raw.githubusercontent.com/conversationai/unhealthy-conversations/main/corpus/train.csv',
            'val':'https://raw.githubusercontent.com/conversationai/unhealthy-conversations/main/corpus/val.csv'}

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    for dataset, url in URLS.items():
        filename = f'{dataset}.csv'
        download_file(url, directory, filename)
    
    files = glob.glob(f'{directory}/*.csv')
    data = defaultdict(list)
    
    attributes = ['antagonize', 'condescending', 'dismissive', 'generalisation', 'generalisation_unfair', 'healthy', 'hostile', 'sarcastic']
    for file in files:
        df = pd.read_csv(file)
        for attr in attributes:
            data[attr].extend(df[df[attr] == 1]['comment'].tolist())
            data['not_' + attr].extend(df[df[attr] == 0]['comment'].tolist())

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_reuters_authorship():
    """
    Downloads and formats data on Reuters authors.
    """

    NAME = 'reuters_authorship'
    TYPE = 'correlation'
    DESC = 'Dataset includes example articles from various Reuters authors on the same topics.'
    URL = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00217/C50.zip'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_zip(URL, directory)
    
    files = glob.glob(f'{directory}/**/**/*.txt')
    data = defaultdict(list)
    for file in files:
        author = file.split('/')[3]
        with open(file, 'r') as f:
            text = f.read()
            data[author].append(text)
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_twitter_mispellings():
    """
    Downloads and formats dataset of Tweets with and without mispellings.
    """
    
    NAME = 'twitter_mispellings'
    TYPE = 'correlation'
    DESC = 'Dataset includes tweets with and without certain mispellings.'
    ID = '0B04GJPshIjmPRnZManQwWEdTZjg'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_drive_zip(ID, directory)

    df = pd.read_csv(join(directory, 'training.1600000.processed.noemoticon.csv'),
      names=['id', 'timstamp', 'type', 'user', 'text'], encoding='latin-1')

    normalization_pairs = [
        ('your', [' ur '], [' your ', ' you\'re ']),
        ('with', [' wit '], [' with ']),
        ('that', [' dat ', ' dats '], [' that ']),   
        ('going', [' goin '], ['going ']),
        ('know', [' kno '], [' know ']),
        ('you', [' u '], [' you ']),
        ('what', [' wut ', ' wat '], [' what ']),
        ('the', [' da '], [' the '])
    ]

    data = {}
    for group, misspell, proper in normalization_pairs:
        data[group + '_misspell'] = df[df['text'].str.contains('|'.join(misspell))]['text'].tolist()
        data[group + '_proper'] = df[df['text'].str.contains('|'.join(proper))]['text'].tolist()
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_reddit_humor():
    """
    Downloads and formats dataset of jokes on Reddit.
    """

    NAME = 'reddit_humor'
    TYPE = 'correlation'
    DESC = 'Dataset includes jokes on Reddit, with funniness judged by the number of upvotes.'
    URLS = {'dev':'https://raw.githubusercontent.com/orionw/RedditHumorDetection/master/data/dev.tsv',
            'test':'https://raw.githubusercontent.com/orionw/RedditHumorDetection/master/data/dev.tsv'}
    
    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    for dataset, url in URLS.items():
        filename = f'{dataset}.tsv'
        download_file(url, directory, filename)

    files = glob.glob(f'{directory}/*.tsv')
    data = defaultdict(list)

    df = pd.DataFrame()
    for file in files:
        df = df.append(pd.read_csv(file, names=['index', 'funny', 'type', 'text'], encoding='latin-1'))
    df = df.drop(['index', 'type'], axis=1)

    data = {}
    def process(text):
        return text.replace('_____', ' ')
    data['funny'] = df[df['funny'] == 1]['text'].apply(process).tolist()
    data['unfunny'] = df[df['funny'] == 0]['text'].apply(process).tolist()

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)
    
def prepare_echr_decisions():
    """
    Downloads and formats dataset of decisions from the European Court of Human Rights (ECHR).
    """

    NAME = 'echr_decisions'
    TYPE = 'causation'
    DESC = 'Dataset includes the facts of each ECHR case and the decision of the judge.'
    URL = 'https://archive.org/download/ECHR-ACL2019/ECHR_Dataset.zip'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_zip(URL, directory)
    
    path = '{directory}/*_Anon/*.json'
    files = glob.glob(path)
    dicts = [json.load(open(f, 'r')) for f in files]

    np.random.seed(0)
    data = defaultdict(list)
    for d in dicts:
        text = '\n'.join(d['TEXT'])
        if d['VIOLATED_ARTICLES']:
            data['violation'].append(text)
        else:
            data['no_violation'].append(text)

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_news_popularity():
    """
    Downloads and formats dataset of decisions from the European Court of Human Rights (ECHR).
    """

    NAME = 'news_popularity'
    TYPE = 'causation'
    DESC = 'Dataset includes various news headlines paired with likes on social media and sentiment.'
    URL = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00432/Data/News_Final.csv'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.csv'
    download_file(URL, directory, filename)

    df = pd.read_csv(join(directory, filename))

    def clean_text(text):
        return str(text).replace('&quot;', '"').replace('"""', '"')

    df['Headline'] = df['Headline'].apply(clean_text)
    df['Title'] = df['Title'].apply(clean_text)

    def top_bottom(group, col, n = 50):
        sorted = group.sort_values(col)
        return sorted.iloc[-n:], sorted.iloc[:n]

    def rank_sentiment(group):
        return top_bottom(group, 'SentimentTitle')

    def rank_fb(group):
        return top_bottom(group, 'Facebook')

    sentiment_groups = df.groupby('Topic').apply(rank_sentiment)
    data = {}
    for topic in sentiment_groups.keys():
        pos, neg = sentiment_groups[topic]
        data[topic + '_pos'] = pos['Title'].tolist()
        data[topic + '_neg'] = neg['Title'].tolist()

    fb_df = df[(df.Source == 'Bloomberg') & (df.Facebook >= 0) & (df.Topic.isin(['obama', 'economy', 'microsoft']))]
    fb_groups = fb_df.groupby('Topic').apply(rank_fb)
    for topic in fb_groups.keys():
        pop, unpop = fb_groups[topic]
        data[topic + '_pop'] = pop['Title'].tolist()
        data[topic + '_unpop'] = unpop['Title'].tolist()

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_convincing_arguments():
    """
    Downloads and formats dataset of arguments and their ranked convincingness.
    """

    NAME = 'convincing_arguments'
    TYPE = 'causation'
    DESC = 'Dataset includes arguments on a variety of topics annotated for convincingness.'
    URL = 'https://github.com/UKPLab/acl2016-convincing-arguments/archive/master.zip'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_zip(URL, directory)

    data_path = f'{directory}/data/UKPConvArg1-Ranking-CSV/*'
    files = glob.glob(data_path)
    df = pd.DataFrame(columns=['id', 'rank', 'argument'])
    def read_file(file):
        f = open(file, 'r')
        lines = f.readlines()
        data = []
        for line in lines[1:]:
            id, rank, argument = line.split('\t')
            data.append([id, rank, argument])
        return pd.DataFrame(data, columns=['id', 'rank', 'argument'])
    for file in files:
        df = df.append(read_file(file))

    def top_bottom(group, col, n=50):
        sorted = group.sort_values(col)
        return sorted.iloc[-n:], sorted.iloc[:n]

    data = {}
    unconvincing, convincing = top_bottom(df, 'rank', 500)
    data['unconvincing'] = unconvincing['argument'].tolist()
    data['convincing'] = convincing['argument'].tolist()

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_microedit_humor():
    """
    Downloads and formats dataset of funny statements generated by one-word substitutions.
    """

    NAME = 'microedit_humor'
    TYPE = 'causation'
    DESC = 'Dataset includes statements rated for humor generated by making one-word edits to normal statements.'
    URL = 'https://cs.rochester.edu/u/nhossain/semeval-2020-task-7-dataset.zip'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_zip(URL, directory)

    files = glob.glob(f'{directory}/**/subtask-1/*.csv')

    df = pd.DataFrame()

    for file in files:
        df = df.append(pd.read_csv(file))
        
    def make_edit(sentence, replacement):
        return re.sub('<[^\>]+>', replacement, sentence)


    df['edited'] = df.apply(lambda x: make_edit(x.original, x.edit), axis=1)
    df['edited'] = df['edited'].apply(clean_text)
    df['bin'] = pd.cut(df['meanGrade'], 3, labels=range(3))
    print(df)
    
    data = {}
    for i, rank in enumerate(['unfunny', 'neutral', 'funny', 'very_funny']):
        data[rank] = df[df['bin'] == i]['edited'].tolist()
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_open_review():
    """
    Scrapes and formats dataset of Open Review papers from ICLR 2018-2021.
    """
    NAME = 'open_review'
    TYPE = 'causation'
    DESC = 'Dataset of ICLR submissions from 2018 and 2021 split on whether they recieved an average rating greater than 5.'

    import scrape_open_review
    good_papers, bad_papers = scrape_open_review.scrape()

    data = {
        'good_papers':good_papers,
        'bad_papers':bad_papers
    }
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_essay_scoring():
    """
    Scrapes and formats essay scoring dataset.
    """

    NAME = 'essay_scoring'
    TYPE = 'causation'
    DESC = 'Dataset of hand-scored essays.'
    URL = 'https://raw.githubusercontent.com/Turanga1/Automated-Essay-Scoring/master/training_set_rel3.tsv'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.tsv'
    download_file(URL, directory, filename)

    df = pd.read_csv(join(directory, filename), sep='\t', encoding='latin-1')
    df = df[df.essay_set == 5]
    good_essays = df[df.domain1_score >= 3].essay.tolist()
    bad_essays = df[df.domain1_score < 3].essay.tolist()

    data = {
        'good_essays':good_essays,
        'bad_essays':bad_essays
    }
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_short_answer_scoring():
    """
    Scrapes and formats short answer scoring dataset.
    """

    NAME = 'short_answer_scoring'
    TYPE = 'causation'
    DESC = 'Dataset of hand-scored short answers.'
    URL = 'https://raw.githubusercontent.com/abdelrahmanelnaka/AraScore-Dataset/master/Question%201DataSet.csv'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.tsv'
    download_file(URL, directory, filename)

    df = pd.read_csv(join(directory, filename), encoding='utf-8')
    df = df[df.EssaySet == 1]
    df['average_score'] = df[['Score1', 'Score2']].mean(axis=1)
    good_essays = df[df.average_score >= 2.5].EssayText.tolist()
    medium_essays = df[(1.5 <= df.average_score) & (df.average_score < 2.5)].EssayText.tolist()
    bad_essays = df[df.average_score < 1.5].EssayText.tolist()

    data = {
        'good_essays':good_essays,
        'medium_essays':medium_essays,
        'bad_essays':bad_essays,
    }
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_tweet_gender():
    """
    Downloads and formats a dataset on Twitter user gender.
    """

    NAME = 'tweet_gender'
    TYPE = 'correlation'
    DESC = 'Dataset of random Tweets with annotations for user gender.'
    URL = 'https://raw.githubusercontent.com/tranctan/Gender-Classification-based-on-Twritter-textual-data/master/gender_dataset.csv'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.tsv'
    download_file(URL, directory, filename)

    df = pd.read_csv(join(directory, filename), encoding='latin-1')
    df = df[df['gender:confidence'] == 1.00]
    male_tweets = df[df.gender=='male'].text.tolist()
    female_tweets = df[df.gender=='female'].text.tolist()

    data = {
        'male_tweets':male_tweets,
        'female_tweets':female_tweets
    }
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_npt_conferences():
    """
    Downloads and formats a dataset of statements from NPT conferences.
    """

    NAME = 'npt_conferences'
    TYPE = 'correlation'
    DESC = 'Dataset of NPT conference transcripts across time.'

    files = glob.glob(f'{MANUAL_FOLDER}/BarnumLoNPTReplication/data/docs_by_committee/**/*.txt')
    docs = []
    for file in files:
        year = re.findall('\d\d\d\d', file)[0]
        with open(file, 'r', encoding='latin1') as f:
            text = " ".join(f.readlines())
        doc = {
            'year':int(year),
            'text':text
        }
        docs.append(doc)

    df = pd.DataFrame(docs)
    pre_2008 = df[df.year < 2008].text.tolist()
    btw_2008_2012 = df[(df.year >= 2008) & (df.year < 2012)].text.tolist()
    post_2012 = df[df.year >= 2012].text.tolist()

    data = {
        'pre_2008':pre_2008,
        'btw_2008_2012':btw_2008_2012,
        'post_2012':post_2012,
    }

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

"""
******
Driver
******
"""

preparers = {
    'open_deception':prepare_open_deception,
    'fake_news':prepare_fake_news,
    'trial_deception':prepare_trial_deception,
    'parenting_subreddits':prepare_parenting_subreddits,
    'diplomacy_deception':prepare_diplomacy_deception,
    'abc_headlines':prepare_abc_headlines,
    'times_india_headlines':prepare_times_india_headlines,
    'clickbait_headlines':prepare_clickbait_headlines,
    'stock_news':prepare_stock_news,
    'unhealthy_conversations':prepare_unhealthy_conversations,
    'reuters_authorship':prepare_reuters_authorship,
    'twitter_mispellings':prepare_twitter_mispellings,
    'reddit_humor':prepare_reddit_humor,
    'echr_decisions':prepare_echr_decisions,
    'news_popularity':prepare_news_popularity,
    'convincing_arguments':prepare_convincing_arguments,
    'rate_my_prof':prepare_rate_my_prof,
    'microedit_humor':prepare_microedit_humor,
    'prepare_open_review':prepare_open_review,
    'essay_grading':prepare_essay_scoring,
    'short_answer_grading':prepare_short_answer_scoring,
    'tweet_gender':prepare_tweet_gender,
    'npt_conferences':prepare_npt_conferences,
}

def main():

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    prepare_npt_conferences()

    if False:
        pbar = tqdm(preparers.items())
        for dataset, prepare_func in pbar:
            pbar.set_description(f'processing {dataset}')
            prepare_func()

        delete_downloads()

"""
*********
Utilities
*********
"""

def download_zip(url: str, directory: str):
    """
    Downloads and extracts contents of a zip folder.
    """

    req = requests.get(url)
    zip = zipfile.ZipFile(BytesIO(req.content))
    zip.extractall(directory)

def download_tar(url: str, directory: str):
    """
    Downloads and extracts contents of a tar file.
    """

    response = requests.get(url, stream=True)
    file = tarfile.open(fileobj=response.raw, mode="r|gz")
    file.extractall(path=directory)

def download_file(url: str, directory: str, filename: str):
    """
    Downloads and names file.
    """
    req = requests.get(url)
    os.makedirs(directory, exist_ok=True)
    with open(join(directory, filename), 'wb') as f:
        f.write(req.content)

def download_drive_zip(id: str, directory: str):
    """
    Downloads files from Google Drive.
    """

    url = f'https://drive.google.com/uc?id={id}'
    os.makedirs(directory, exist_ok=True)
    gdown.download(url, join(directory, 'drive.zip'))
    with zipfile.ZipFile(join(directory, 'drive.zip'), 'r') as zip_ref:
        zip_ref.extractall(directory)

def format_data(data: Dict, type: str, desc: str) -> Dict:
    """
    Formats dataset with type and descripiton to a final output.
    """

    output = {
        'description':desc,
        'type':type,
        'data':data,
    }
    return output

def save_json(output: Dict, name: str):
    """
    Saves output data to output folder.
    """

    output_file = f'{OUTPUT_FOLDER}/{name}.json'
    with open(output_file, 'w') as outfile:
        json.dump(output, outfile)

def delete_downloads():
    """
    Clears the downloads folder.
    """

    shutil.rmtree(DOWNLOAD_FOLDER)

def clean_text(text):
    """
    Repalces common unicode characters.
    """
    return text.encode("ascii", "ignore").decode()

if __name__ == '__main__':
    main()