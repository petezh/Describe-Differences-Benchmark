import codecs
from collections import defaultdict
import itertools
import json
import os
from os.path import join
import re

import glob
import numpy as np
import pandas as pd
from tqdm import tqdm

from parameters import *
from utils import *

"""
**********
Preparers
**********
"""

def prepare_open_deception():
    """Downloads and formats the Open Deception dataset."""
    
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
    """Downloads and formats the Fake News dataset."""
    
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
    """Downloads and formats the Real-life Deception dataset."""

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
            contents = encode_ascii(f.read())
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
    """Downloads and formats Rate My Professor dataset."""

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
    df['comments'] = df['comments'].apply(lambda s: codecs.unicode_escape_decode(s)[0] if isinstance(s, str) else "")
    df['first_name'] = df['professor_name'].str.split().str[0]
    df['gender'] = df['first_name'].apply(get_gender)
    df['gender'].value_counts()

    df = df.sample(frac=1, random_state = 0)

    data = {
        'female':list(map(str, df[df['gender']=='female']['comments'])),
        'male':list(map(str, df[df['gender']=='male']['comments']))
    }

    data['female'] = list(filter(None, [t for t in data['female'] if ' him ' not in t and ' his ' not in t]))
    data['male'] = list(filter(None, [t for t in data['male'] if ' she ' not in t and ' her ' not in t]))

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_parenting_subreddits():
    """Downloads and formats parenting discussion threads on Reddit."""

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
        clean_text = text.apply(lambda s: codecs.unicode_escape_decode(s)[0]).apply(encode_ascii)
        data[topic] = clean_text.tolist()

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_diplomacy_deception():
    """Downloads and formats deception data from rounds of the game, Diplomacy."""

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

    def clean(text):
        return encode_ascii(text).replace('\n', '')

    for file in files:
        df = pd.read_json(file, lines=True)
        messages = list(itertools.chain.from_iterable(pd.read_json(files[0], lines=True)['messages']))
        labels = list(itertools.chain.from_iterable(pd.read_json(files[0], lines=True)['sender_labels']))
        df = pd.DataFrame({'message':messages, 'label':labels})
        data['truth'].extend(df[df['label']==True]['message'].apply(clean).tolist())
        data['lie'].extend(df[df['label']==False]['message'].apply(clean).tolist())
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_abc_headlines():
    """Downloads and formats a million headlines from ABC news."""

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
    """Downloads and formats a million headlines from Times of India news."""

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
    """Downloads and formats a million headlines from The Examiner, a clickbait news site."""

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
    """Downloads and formats a million headlines from The Examiner, a clickbait news site."""

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
    """Downloads and formats data on unhealthy conversations."""

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
    """Downloads and formats data on Reuters authors."""

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

def prepare_twitter_misspellings():
    """Downloads and formats dataset of Tweets with and without misspellings."""
    
    NAME = 'twitter_misspellings'
    TYPE = 'correlation'
    DESC = 'Dataset includes tweets with and without certain misspellings.'
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
    """Downloads and formats dataset of jokes on Reddit."""

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
        return encode_ascii(text.replace('_____', ' '))
    data['funny'] = df[df['funny'] == 1]['text'].apply(process).tolist()
    data['unfunny'] = df[df['funny'] == 0]['text'].apply(process).tolist()

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)
    
def prepare_echr_decisions():
    """Downloads and formats dataset of decisions from the European Court of Human Rights (ECHR)."""

    NAME = 'echr_decisions'
    TYPE = 'causation'
    DESC = 'Dataset includes the facts of each ECHR case and the decision of the judge.'
    URL = 'https://archive.org/download/ECHR-ACL2019/ECHR_Dataset.zip'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_zip(URL, directory)
    
    path = f'{directory}/*_Anon/*.json'

    np.random.seed(0)
    files = np.random.choice(glob.glob(path), 500, replace=False)
    dicts = [json.load(open(f, 'r')) for f in files]

    
    data = defaultdict(list)
    for d in dicts:
        text = list(d['TEXT'])
        if d['VIOLATED_ARTICLES']:
            data['violation'].extend(text)
        else:
            data['no_violation'].extend(text)

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_news_popularity():
    """Downloads and formats dataset of news headlines and popularity."""

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

    def top_bottom(group, col, n = 100):
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
    """Downloads and formats dataset of arguments and their ranked convincingness."""

    NAME = 'convincing_arguments'
    TYPE = 'causation'
    DESC = 'Dataset includes arguments on a variety of topics annotated for convincingness.'
    URL = 'https://github.com/UKPLab/acl2016-convincing-arguments/archive/master.zip'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_zip(URL, directory)

    data_path = f'{directory}/acl2016-convincing-arguments-master/data/UKPConvArg1-Ranking-CSV/*'
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

    def clean(text):
        return strip_tags(text).replace('\n', '')
    
    df['argument'] = df['argument'].apply(clean)

    data = {}
    unconvincing, convincing = top_bottom(df, 'rank', 200)
    data['unconvincing'] = unconvincing['argument'].tolist()
    data['convincing'] = convincing['argument'].tolist()

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_microedit_humor():
    """Downloads and formats dataset of funny statements generated by one-word substitutions."""

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
    df['bin'] = pd.cut(df['meanGrade'], 4, labels=range(4))
    
    data = {}
    for i, rank in enumerate(['unfunny', 'neutral', 'funny', 'very_funny']):
        data[rank] = df[df['bin'] == i]['edited'].tolist()
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_open_review():
    """Scrapes and formats dataset of Open Review papers from ICLR 2018-2021."""
    NAME = 'open_review'
    TYPE = 'causation'
    DESC = 'Dataset of ICLR submissions from 2018 and 2021 split on whether they recieved an average rating greater than 5.'

    import scrape_open_review
    great_papers, good_papers, bad_papers = scrape_open_review.scrape()

    data = {
        'great_papers':list(map(encode_ascii, great_papers)),
        'good_papers':list(map(encode_ascii, good_papers)),
        'bad_papers':list(map(encode_ascii, bad_papers)),
    }
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_essay_scoring():
    """Scrapes and formats essay scoring dataset."""

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
    """Scrapes and formats short answer scoring dataset."""

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
    good_answers = df[df.average_score >= 2.5].EssayText.tolist()
    medium_answers = df[(1.5 <= df.average_score) & (df.average_score < 2.5)].EssayText.tolist()
    bad_answers = df[df.average_score < 1.5].EssayText.tolist()

    data = {
        'good_answers':good_answers,
        'medium_answers':medium_answers,
        'bad_answers':bad_answers,
    }
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_tweet_gender():
    """Downloads and formats a dataset on Twitter user gender."""

    NAME = 'tweet_gender'
    TYPE = 'correlation'
    DESC = 'Dataset of random Tweets with annotations for user gender.'
    URL = 'https://raw.githubusercontent.com/tranctan/Gender-Classification-based-on-Twritter-textual-data/master/gender_dataset.csv'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.tsv'
    download_file(URL, directory, filename)

    df = pd.read_csv(join(directory, filename), encoding='latin-1')
    df = df[df['gender:confidence'] == 1.00]
    df['text'] = df['text'].apply(encode_ascii)
    male_tweets = df[df.gender=='male'].text.tolist()
    female_tweets = df[df.gender=='female'].text.tolist()

    data = {
        'male_tweets':male_tweets,
        'female_tweets':female_tweets
    }
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_npt_conferences():
    """Downloads and formats a dataset of statements from NPT conferences."""

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

    def prep_list(text):
        para_list = []
        for t in text:
            paras = t.replace('\t', ' ').split('\n')
            para_list.extend([p for p in filter(None, paras) if len(p) > 50])
        return para_list

    pre_2008 = prep_list(df[df.year < 2008].text)
    btw_2008_2012 = prep_list(df[(df.year >= 2008) & (df.year < 2012)].text)
    post_2012 = prep_list(df[df.year >= 2012].text)

    data = {
        'pre_2008':pre_2008,
        'btw_2008_2012':btw_2008_2012,
        'post_2012':post_2012,
    }

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_twitter_rumors():
    """Downloads and prepares a dataset of Twitter rumors."""

    NAME = 'tweet_rumor'
    TYPE = 'correlation'
    DESC = 'Dataset of rumors over time on various topics.'

    import scrape_twitter_rumors

    data = scrape_twitter_rumors.scrape()
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_armenian_jobs():
    """Downloads and engineers features for dataset of Armenian job postings."""

    NAME = 'armenian_jobs'
    TYPE = 'correlation'
    DESC = 'Dataset of job postings in Armenia by role and year.'
    URL = 'https://raw.githubusercontent.com/GurpreetKaur28/Analysing-Online-Job-Postings/master/data%20job%20posts.csv'
    
    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.tsv'
    download_file(URL, directory, filename)

    df = pd.read_csv(join(directory, filename))

    data = {}

    jobs = {
        'sw_dev':'Software Developer',
        'senior_sw_dev':'Senior Software Developer',
        'qa_eng':'QA Engineer',
        'senior_qa_eng':'Senior QA Engineer',
        'sw_eng':'Software Engineer',
        'senior_sw_eng':'Senior Software Engineer',
        'java_dev':'Java Developer',
        'senior_java_dev':'Senior Java Developer',
        'prgmr':'programmer',
    }

    def clean(text):
        return str(text).replace('\n', ' ')

    df['JobDescription'] = df['JobDescription'].apply(clean)
    df['JobRequirment'] = df['JobRequirment'].apply(clean)

    for name, title in jobs.items():
        descriptions = df[df.Title == title]['JobDescription'].dropna().tolist()
        requirements =  df[df.Title == title]['JobRequirment'].dropna().tolist()
        data[f'job_desc_{name}'] = descriptions
        data[f'job_req_{name}'] = requirements

    year_bins = [(2004, 2007), (2007, 2010), (2010, 2013), (2013, 2015)]
    for start_year, end_year in year_bins:
        requirements = df[(start_year <= df.Year) & (df.Year < end_year)]['JobRequirment'].dropna().tolist()
        app_process = df[(start_year <= df.Year) & (df.Year < end_year)]['ApplicationP'].dropna().tolist()
        data[f'job_req_years_{start_year}_{end_year}'] = requirements
        data[f'app_process_years_{start_year}_{end_year}'] = app_process

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_monster_jobs():
    """Downloads and engineers features for dataset of job postings on Monster.com."""

    NAME = 'monster_jobs'
    TYPE = 'correlation'
    DESC = 'Dataset of job postings on monster.com by geography.'

    df = pd.read_csv(join(MANUAL_FOLDER, 'monster_com-job_sample.csv'))
    
    locations = {
        'dallas':'Dallas, TX',
        'houston':'Houston, TX',
        'austin':'Austin, TX',
        'denver':'Denver, CO',
        'atlanta':'Atlanta, GA',
        'cincinatti':'Cincinnati, OH',
        'tampa':'Tampa, FL',
        'boston':'Boston, MA',
        'milwaukee':'Milwaukee, WI',
        'la':'Los Angeles, CA',
        'sf':'San Francisco, CA',
        'nashville':'Nashville, TN',
        'nyc':'New York, NY',
        'colombus':'Columbus, OH',
        'seattle':'Seattle, WA',
        'las_vegas':'Las Vegas, NV',
        'berkeley':'Berkeley, CA'
    }

    def clean(text):
        return encode_ascii(text).replace('\n', '')

    df['job_description'] = df['job_description'].apply(clean)

    data = {}
    for name, loc in locations.items():
        descriptions = df[df.location.str.contains(loc)].job_description.dropna().tolist()
        data[name] = descriptions

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)


def prepare_dice_jobs():
    """Downloads and engineers features for dataset of job postings on dice.com."""

    NAME = 'dice_jobs'
    TYPE = 'correlation'
    DESC = 'Dataset of job postings on dice.com grouped by leading employers.'

    df = pd.read_csv(join(MANUAL_FOLDER, 'Dice_US_jobs.csv'), encoding='latin-1')
    orgs = {
        'northup_grumman':'NORTHROP GRUMMAN',
        'leidos':'Leidos',
        'dell':'Dell',
        'deloitte':'Deloitte',
        'amazon':'Amazon',
        'jpm':'JPMorgan Chase'
    }

    def clean(text):
        return text.replace('\u00e5\u00ca', '')
    
    df['job_description'] = df['job_description'].apply(clean)

    data = {}
    for name, org in orgs.items():
        descriptions = df[df.organization == org].job_description.dropna().tolist()
        data[name] = descriptions

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_admin_statements():
    """
    Downloads and formats dataset of White House administration statements.
    """

    NAME = 'admin_statements'
    TYPE = 'correlation'
    DESC = 'Dataset includes statements of administration policy for three presidents.'
    URL = 'https://github.com/unitedstates/statements-of-administration-policy/archive/master.zip'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_zip(URL, directory)
    
    import scrape_admin_statements

    data = scrape_admin_statements.scrape()

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_suicide_notes():
    """Download and formats dataset of Reddit posts about suicide and depression."""

    NAME = 'suicide_notes'
    TYPE = 'correlation'
    DESC = 'Dataset is composed of posts from r/SuicideWatch and r/depression.'
    URL = 'https://raw.githubusercontent.com/hesamuel/goodbye_world/master/data/data_for_model_2.csv'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.csv'
    download_file(URL, directory, filename)
    
    df = pd.read_csv(join(directory, filename))
    df['all_text'] = df['title'] + ' ' + df['selftext']
    data = {
        'depression':df[df.is_suicide == 0].all_text.tolist(),
        'suicide':df[df.is_suicide == 1].all_text.tolist(),
    }

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_reddit_stress():
    """Downloads and formats subsample of the Dreaddit dataset."""
    
    NAME = 'reddit_stress'
    TYPE = 'correlation'
    DESC = 'Dataset is composed of stress-related posts on Reddit.'
    URL = 'https://raw.githubusercontent.com/gillian850413/Insight_Stress_Analysis/master/data/dreaddit-train.csv'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.csv'
    download_file(URL, directory, filename)
    
    df = pd.read_csv(join(directory, filename), encoding='latin-1')

    data = {
    'ptsd':df[df.subreddit == 'ptsd'].text.tolist(),
    'anxiety':df[df.subreddit == 'anxiety'].text.tolist(),
    'stress':df[df.subreddit == 'stress'].text.tolist(),
    }

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_drug_experiences():
    """Downloads and formats self-reported drug expeirences from Erowid.com."""

    NAME = 'drug_experiences'
    TYPE = 'correlation'
    DESC = 'Dataset comprises self-reports of various drugs scraped from Erowid.com.'
    URL = 'https://github.com/technillogue/erowid-w2v/archive/master.zip'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    download_zip(URL, directory)

    DRUGS = ['cocaine', 'dxm', 'lsd', 'mdma', 'mushrooms', 'oxycodone', 'salvia', 'tobacco']

    data = {}

    for drug in DRUGS:
        
        files = glob.glob(join(directory, f'erowid-w2v-master/core-experiences/{drug}/*'))
        experiences = []

        for file in files:
            with open(file, 'r') as f:
                text = "".join(f.readlines())
                text = strip_tags(text).replace('\r', '').split('\n')
                experiences.extend([p for p in filter(None, text) if len(p) > 50])
        
        data[drug] = experiences
    
    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_oral_histories():
    """Downloads and formats transcribed oral histories."""
    
    NAME = 'oral_histories'
    TYPE = 'correlation'
    DESC = 'Dataset is composed of oral histories transcribed by OHTAP'
    URL = 'https://raw.githubusercontent.com/ohtap/ohtap/master/Research%20Question%202/updated_0510.csv'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    filename = f'{NAME}.csv'
    download_file(URL, directory, filename)
    
    df = pd.read_csv(join(directory, filename), sep='\t')
    southern_states = """MD
    DE
    VA
    WV
    KY
    TN
    NC
    SC
    FL
    GA
    AL
    MS
    LA
    AK
    TX
    OK""".split('\n')

    df['corrected_text'] = df['corrected_text'].apply(encode_ascii)

    data = {
        'pre_1930':df[df.birth_year < 1930].corrected_text.to_list(),
        '1930-50':df[(df.birth_year >= 1930) & (df.birth_year < 1950)].corrected_text.to_list(),
        'post_1950':df[df.birth_year > 1950].corrected_text.to_list(),
        'black':df[df.race == 'Black or African American'].corrected_text.to_list(),
        'white':df[df.race == 'White'].corrected_text.to_list(),
        'asian':df[df.race == 'Asian'].corrected_text.to_list(),
        'college_educated':df[df.education.isin(['Graduate or professional degree', 'Bachelor\'s degree'])].corrected_text.to_list(),
        'not_college_educated':df[~df.education.isin(['Graduate or professional degree', 'Bachelor\'s degree'])].corrected_text.to_list(),
        'south':df[df.interviewee_birth_state.isin(southern_states)].corrected_text.to_list(),
        'not_south':df[~df.interviewee_birth_state.isin(southern_states)].corrected_text.to_list(),
    }

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_fomc_speeches():
    """Downloads and formats FOMC speeches annotated with economic indicators."""
    
    NAME = 'fomc_speeches'
    TYPE = 'correlation'
    DESC = 'Dataset is composed of FOMC speeches from 1996-2020'

    df = pd.read_csv(f'{MANUAL_FOLDER}/fed_speeches_1996_2020.csv')
    df = df.dropna()
    df['year_month'] = df['date'].astype(int).astype(str).str[:6]
    indicators_df = pd.read_csv(f'{MANUAL_FOLDER}/macro_indicators.csv')

    indicators_df['year_month'] = indicators_df.Date.astype(str).str[:6]
    df = df.merge(indicators_df, on='year_month', how='left')
    bins = 5
    df['unemp_cuts'] = pd.qcut(df['unemployment'], q=bins, labels=range(bins))
    df['growth_cuts'] = pd.qcut(df['growth rate'], q=bins, labels=range(bins))
    df['ir_cuts'] = pd.qcut(df['fed interest rate'], q=bins, labels=range(bins))

    data = {
        'greenspan_speeches':df[df.speaker == 'Chairman Alan Greenspan'].text.str.strip().tolist(),
        'bernanke_speeches':df[df.speaker == 'Chairman Ben S. Bernanke'].text.str.strip().tolist(),
        'greenspan_years':df[df.year_month <= '200601'].text.str.strip().tolist(),
        'bernanke_years':df[(df.year_month >= '200602') & (df.year_month <= '201401')].text.str.strip().tolist(),
        'yellen_years':df[(df.year_month >= '201402') & (df.year_month <= '201801')].text.str.strip().tolist(),
        'powell_years':df[df.year_month >= '201802'].text.str.strip().tolist(),
        'low_unemp':df[df.unemp_cuts == 0].text.str.strip().tolist(),
        'high_unemp':df[df.unemp_cuts == bins-1].text.str.strip().tolist(),
        'low_growth':df[df.growth_cuts == 0].text.str.strip().tolist(),
        'high_growth':df[df.growth_cuts == bins-1].text.str.strip().tolist(),
        'low_ir':df[df.ir_cuts == 0].text.str.strip().tolist(),
        'high_ir':df[df.ir_cuts == bins-1].text.str.strip().tolist(),
    }

    output = format_data(data, TYPE, DESC)
    save_json(output, NAME)

def prepare_ad_transcripts():
    """Downloads and formats a dataset of almost 2,000 ad scripts."""
    
    NAME = 'ad_transcripts'
    TYPE = 'correlation'
    DESC = 'Dataset is composed of nearly 2,000 ad scripts from a variety of industries.'

    df = pd.read_excel(f'{MANUAL_FOLDER}/Advertisement_Transcripts_deduped_edited.xlsx')
    top_n = 8
    industries = df.Category.value_counts().index[:top_n].tolist()

    def clean(text):
        return text.replace('\n', ' ')

    data = {}
    for industry in industries:
        data[industry] = df[df.Category == industry].Ad_copy.apply(clean).to_list()

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
    'twitter_mispellings':prepare_twitter_misspellings,
    'reddit_humor':prepare_reddit_humor,
    'echr_decisions':prepare_echr_decisions,
    'news_popularity':prepare_news_popularity,
    'convincing_arguments':prepare_convincing_arguments,
    'rate_my_prof':prepare_rate_my_prof,
    'microedit_humor':prepare_microedit_humor,
    'prepare_open_review':prepare_open_review,
    'essay_scoring':prepare_essay_scoring,
    'short_answer_scoring':prepare_short_answer_scoring,
    'tweet_gender':prepare_tweet_gender,
    'npt_conferences':prepare_npt_conferences,
    'twitter_rumors':prepare_twitter_rumors,
    'armenian_jobs':prepare_armenian_jobs,
    'monster_jobs':prepare_monster_jobs,
    'dice_jobs':prepare_dice_jobs,
    'admin_statements':prepare_admin_statements,
    'suicide_notes':prepare_suicide_notes,
    'reddit_stress':prepare_reddit_stress,
    'drug_experiences':prepare_drug_experiences,
    'oral_histories':prepare_oral_histories,
    'fomc_speeches':prepare_fomc_speeches,
    'ad_transcripts':prepare_ad_transcripts,
}

def main():

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    prepare_ad_transcripts()

    if False:
        pbar = tqdm(preparers.items())
        for dataset, prepare_func in pbar:
            pbar.set_description(f'processing {dataset}')
            prepare_func()

        delete_downloads()

if __name__ == '__main__':
    main()