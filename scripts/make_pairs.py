from itertools import chain
import json
from typing import List

from tqdm import tqdm

from parameters import *

def generate_pair(dataset: str, pos: List[str], neg: List[str], annotations: List[str]):
    path = f'{OUTPUT_FOLDER}/{dataset}.json'
    output = json.load(open(path, 'r'))
    pos_dists = [output['data'][dist] for dist in pos]
    neg_dists = [output['data'][dist] for dist in neg]
    pos_samples = list(chain.from_iterable(pos_dists))
    neg_samples = list(chain.from_iterable(neg_dists))
    return {
        'dataset':dataset,
        'human_annotations':annotations,
        'positive_samples':pos_samples,
        'negative_samples':neg_samples
    }

def describe_pair(pair):
    print('dataset:',pair['dataset'])
    print('# annotations:',len(pair['human_annotations']))
    print('# pos samples:',len(pair['positive_samples']))
    print('# neg samples:',len(pair['negative_samples']))

def pair_abc_headlines_2007_2008():
    """ABC news headlines from 2007 and 2008."""

    DATASET = 'abc_headlines'
    POS = ['2007']
    NEG = ['2008']
    ANNOTATIONS = ['talks less about the economy']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_abc_headlines_2019_2020():
    """ABC news headlines from 2019 and 2020."""

    DATASET = 'abc_headlines'
    POS = ['2019']
    NEG = ['2020']
    ANNOTATIONS = ['talks less about COVID-19', 'more positive']
    
    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_ad_transcripts_automative_travel():
    """Ad transcripts for automobile and travel companies."""

    DATASET = 'ad_transcripts'
    POS = ['Automotive']
    NEG = ['Travel']
    ANNOTATIONS = ['talks more about performance','talks more about family']
    
    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_ad_transcripts_beauty_care():
    """Ad transcripts for beauty products and personal care products."""

    DATASET = 'ad_transcripts'
    POS = ['Beauty']
    NEG = ['Home & Personal Care']
    ANNOTATIONS = ['talks more about seeing','talks more about fashion']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_admin_statements_obama_biden():
    """Administration statements from Obama and Biden."""

    DATASET = 'admin_statements'
    POS = ['44-Obama']
    NEG = ['46-Biden']
    ANNOTATIONS = ['talks more about the economy', 'talks less about COVID-19']
    
    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_admin_statements_trump_biden():
    """Administration statements from Trump and Biden."""

    DATASET = 'admin_statements'
    POS = ['45-Trump']
    NEG = ['46-Biden']
    ANNOTATIONS = ['talks more about immigration', 'favor conservative policies', 'talks less about COVID-19']
    
    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_armenian_jobs_sw_qa():
    """Armenian job postings for software vs. QA positions."""

    DATASET = 'armenian_jobs'
    POS = ['job_desc_sw_dev','job_desc_senior_sw_dev','job_desc_sw_eng','job_desc_senior_sw_eng']
    NEG = ['job_desc_qa_eng','job_desc_senior_qa_eng']
    ANNOTATIONS = ['talks less about testing','talks more about development']
    
    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_armenian_jobs_junior_senior():
    """Armenian job postings for junior vs. senior positions."""

    DATASET = 'armenian_jobs'
    POS = ['job_req_senior_sw_dev','job_req_senior_sw_eng','job_req_senior_qa_eng']
    NEG = ['job_req_qa_eng','job_req_sw_eng','job_req_sw_dev',]
    ANNOTATIONS = ['reqiures more experience','talks about senior positions']
    
    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_armenian_jobs_pre_post_recession():
    """Armenian job postings for 2004-2006 and 2007-2009."""

    DATASET = 'armenian_jobs'
    POS = ['job_req_years_2004_2007']
    NEG = ['job_req_years_2007_2010',]
    ANNOTATIONS = ['requires more experience','talks less about technology']
    
    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_armenian_jobs_reqs_pre_post_2012():
    """Armenian job posting requirements for 2010-2012 and 2013-2014."""
    
    DATASET = 'armenian_jobs'
    POS = ['job_req_years_2010_2013']
    NEG = ['job_req_years_2013_2015',]
    ANNOTATIONS = ['requires newer programming languages','requires more education']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_armenian_jobs_apps_pre_post_2012():
    """Armenian job posting application process for 2010-2012 and 2013-2014."""

    DATASET = 'armenian_jobs'
    POS = ['app_process_years_2010_2013']
    NEG = ['app_process_years_2013_2015',]
    ANNOTATIONS = ['talks more about online applications']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_clickbait_headlines_pre_post_2013():
    """Clickbait headlines from the Examiner for 2010-2012 versus 2013-2015."""

    DATASET = 'clickbait_headlines'
    POS = ['2010','2011','2012']
    NEG = ['2013','2014','2015']
    ANNOTATIONS = ['talks more about Mitt Romney']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_convincing_arguments_convincing_unconvincing():
    """Arguments in online forums rated convincing and unconvincing."""

    DATASET = 'convincing_arguments'
    POS = ['convincing']
    NEG = ['unconvincing']
    ANNOTATIONS = ['provides more explanation','gives examples','does not insult others']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_dice_jobs_amazon_dell():
    """Job postings on Dice from Amazon vs. Dell."""

    DATASET = 'dice_jobs'
    POS = ['amazon']
    NEG = ['dell']
    ANNOTATIONS = ['talks more about Java','talks more about software']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_dice_jobs_northup_grumman_leidos():
    """Job postings on Dice from Northup Grumman vs. Leidos."""

    DATASET = 'dice_jobs'
    POS = ['northup_grumman']
    NEG = ['leidos']
    ANNOTATIONS = ['talks more about aerospace']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_dice_jobs_jpm_chase_deloitte():
    """Job postings on Dice from JP Morgan Chase vs. Deloitte."""

    DATASET = 'dice_jobs'
    POS = ['jpm']
    NEG = ['deloitte']
    ANNOTATIONS = ['talks more about banking','talks less about consulting']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_diplomacy_deception_truth_lie():
    """True and false statements during games of Diplomacy."""

    DATASET = 'diplomacy_deception'
    POS = ['truth']
    NEG = ['lie']
    ANNOTATIONS = ['makes fewer requests','praises the other player less']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_drug_experiences_cocaine_molly():
    """Self-reported experiences of users of cocaine and MDMA."""

    DATASET = 'drug_experiences'
    POS = ['cocaine']
    NEG = ['mdma']
    ANNOTATIONS = ['talks more about hallucinations','talks about concerts']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_drug_experiences_lsd_dxm():
    """Self-reported experiences of users of LSD and dextromethorphan (DXM)."""

    DATASET = 'drug_experiences'
    POS = ['lsd']
    NEG = ['dxm']
    ANNOTATIONS = ['more realistic experiences','talks more about visions']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_drug_experiences_lsd_shrooms():
    """Self-reported experiences of users of LSD and mushrooms."""

    DATASET = 'drug_experiences'
    POS = ['lsd']
    NEG = ['mushrooms']
    ANNOTATIONS = ['talks about higher energy','mentions fewer hallucinations']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_echr_decisions_yes_no_violation():
    """ECHR rulings that did or did not find a violation of an article."""

    DATASET = 'echr_decisions'
    POS = ['violation']
    NEG = ['no_violation']
    ANNOTATIONS = ['talks more about witnesses','mentions more violence']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_essay_scoring_good_bad():
    """Essays on the same topic with good or bad scores."""

    DATASET = 'essay_scoring'
    POS = ['good_essays']
    NEG = ['bad_essays']
    ANNOTATIONS = ['has longer sentences','uses longer words','has more words','is more coherent','has fewer spelling mistakes']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_fake_news_fake_legit():
    """News articles that are either fake or legit."""

    DATASET = 'fake_news'
    POS = ['fake']
    NEG = ['legit']
    ANNOTATIONS = ['uses more extreme language','cites fewer sources','is more political']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_fomc_speeches_greenspan_bernanke():
    """FOMC speeches from Chariman Greenspan and Chairman Bernanke."""

    DATASET = 'fomc_speeches'
    POS = ['greenspan_speeches']
    NEG = ['bernanke_speeches']
    ANNOTATIONS = ['calls for more action','talks more about growth','talks less about targets']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_fomc_speeches_greenspan_bernanke_years():
    """FOMC speeches from the terms of Chariman Greenspan (-2006) and Chairman Bernanke (2006-2014)."""

    DATASET = 'fomc_speeches'
    POS = ['greenspan_years']
    NEG = ['bernanke_years']
    ANNOTATIONS = ['calls for more action','talks more about growth','talks less about targets']
    
    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_fomc_speeches_yellen_powell_years():
    """FOMC speeches from the terms of Chariman Yellen (2014-2018) and Chairman Powell (2018-)."""

    DATASET = 'fomc_speeches'
    POS = ['yellen_years']
    NEG = ['powell_years']
    ANNOTATIONS = ['talks more about unemployment','does not mention COVID-19','talks about economic growth']
    
    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_fomc_speeches_unemployment():
    """FOMC speeches during periods of high and low unemployment."""

    DATASET = 'fomc_speeches'
    POS = ['high_unemp']
    NEG = ['low_unemp']
    ANNOTATIONS = ['talks more about unemployment','talks about lowering the interest rate','talks less about inflation']
    
    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_fomc_speeches_growth():
    """FOMC speeches during periods of high and low GDP growth."""

    DATASET = 'fomc_speeches'
    POS = ['high_growth']
    NEG = ['low_growth']
    ANNOTATIONS = ['talks more about inflation','is more optimistic']
    
    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_fomc_speeches_interest_rate():
    """FOMC speeches during periods of high and low fed interest rate."""

    DATASET = 'fomc_speeches'
    POS = ['high_ir']
    NEG = ['low_ir']
    ANNOTATIONS = ['talks more about inflation','worries more about recession']
    
    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_microedit_humor_unfunny_funny():
    """Humor generated from microedits that are either unfunny or funny."""

    DATASET = 'microedit_humor'
    POS = ['unfunny']
    NEG = ['funny']
    ANNOTATIONS = ['is incoherent','is expected']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_microedit_humor_funny_very_funny():
    """Humor generated from microedits that are funny or very funny."""

    DATASET = 'microedit_humor'
    POS = ['funny']
    NEG = ['very_funny']
    ANNOTATIONS = ['is less surprising','uses slapstick humor']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)


def pair_monster_jobs_atl_tampa():
    """Job postings on Monster.com in Atlanta, GA vs. Tampa, FL."""

    DATASET = 'monster_jobs'
    POS = ['atlanta']
    NEG = ['tampa']
    ANNOTATIONS = ['offers blue collar jobs','talks less about the beach']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_monster_jobs_ca_tx():
    """Job postings on Monster.com in California versus Texas."""

    DATASET = 'monster_jobs'
    POS = ['sf','la','berkeley']
    NEG = ['dallas','houston','austin']
    ANNOTATIONS = ['offers tech related jobs','offers more benefits','offers greater compensation']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_monster_jobs_sf_nyc():
    """Job postings on Monster.com in NYC versus San Francisco."""

    DATASET = 'monster_jobs'
    POS = ['nyc']
    NEG = ['sf']
    ANNOTATIONS = ['offers more finance jobs','talks more about location']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_news_popularity_economy_pop_unpop():
    """Popular vs. unpoplar Bloomberg news related to the economy, measured by Facebook engagement."""

    DATASET = 'news_popularity'
    POS = ['economy_pop']
    NEG = ['economy_unpop']
    ANNOTATIONS = ['is about an economic shock','talks about the U.S. economy']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_news_popularity_microsoft_pop_unpop():
    """Popular vs. unpoplar Bloomberg news related to Microsoft, measured by Facebook engagement."""

    DATASET = 'news_popularity'
    POS = ['microsoft_pop']
    NEG = ['microsoft_unpop']
    ANNOTATIONS = ['talks about user privacy','talks about Zuckerberg']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_news_popularity_obama_pop_unpop():
    """Popular vs. unpoplar Bloomberg news related to Obama, measured by Facebook engagement."""

    DATASET = 'news_popularity'
    POS = ['obama_pop']
    NEG = ['obama_unpop']
    ANNOTATIONS = ['talks about Obama negatively','talks about Afghanistan']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)
    
def pair_news_popularity_obama_pos_neg():
    """Positive or negative sentiment news related to Obama."""

    DATASET = 'news_popularity'
    POS = ['obama_pos']
    NEG = ['obama_neg']
    ANNOTATIONS = ['talks about Obamacare','talks about the economy']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_npt_conferences_pre_post_2008():
    """NPT conference reports from before 2008 and between 2008-2012."""

    DATASET = 'npt_conferences'
    POS = ['pre_2008']
    NEG = ['btw_2008_2012']
    ANNOTATIONS = ['mentions Iran','mentions 9/11','talks less about the economy']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_npt_conferences_pre_post_2012():
    """NPT conference reports from between 2008-2012 and after 2012."""

    DATASET = 'npt_conferences'
    POS = ['btw_2008_2012']
    NEG = ['post_2012']
    ANNOTATIONS = ['mentions Russia','talks about hypersonic missiles']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_open_deception_lie_truth():
    """Human generated truths and lies from any domain."""

    DATASET = 'open_deception'
    POS = ['lie']
    NEG = ['truth']
    ANNOTATIONS = ['talks about themselves','uses extreme adjectives']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_open_review_good_bad():
    """Open Review papers that recieved good (5-7) ratings versus bad (<5)."""

    DATASET = 'open_review'
    POS = ['good_papers']
    NEG = ['bad_papers']
    ANNOTATIONS = ['is better written','provides more equations']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_open_review_great_good():
    """Open Review papers that recieved great (8+) versus good (5-7) ratings."""

    DATASET = 'open_review'
    POS = ['great_papers']
    NEG = ['good_papers']
    ANNOTATIONS = ['expresses surprise','introduces a benchmark','introduces a new technique']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_oral_histories_pre_post_1930():
    """Oral histories from people born pre-1930 versus 1930-1950."""

    DATASET = 'oral_histories'
    POS = ['pre_1930']
    NEG = ['1930-50']
    ANNOTATIONS = ['talks more about racism','talks about older presidents','mentions World War I']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_oral_histories_pre_post_1950():
    """Oral histories from people born 1930-1950 versus post-1950."""

    DATASET = 'oral_histories'
    POS = ['1930-50']
    NEG = ['post_1950']
    ANNOTATIONS = ['talks about the Great Depression','mentions World War II']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)
    
def pair_oral_histories_black_white():
    """Oral histories from black versus white people."""

    DATASET = 'oral_histories'
    POS = ['black']
    NEG = ['white']
    ANNOTATIONS = ['talks more about racism','talks more about civil rights','discusses more violence']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_oral_histories_asian_white():
    """Oral histories from Asian versus white people."""

    DATASET = 'oral_histories'
    POS = ['asian']
    NEG = ['white']
    ANNOTATIONS = ['talks more about racism','talks more about civil rights','discusses more violence']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_oral_histories_college_educated():
    """Oral histories from college-educated and non-college-educated people."""

    DATASET = 'oral_histories'
    POS = ['college_educated']
    NEG = ['not_college_educated']
    ANNOTATIONS = ['talks more about academic jobs','mentions civil rights','uses eloquent language']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_oral_histories_south_not_south():
    """Oral histories from people born in the South versus elsewhere."""

    DATASET = 'oral_histories'
    POS = ['south']
    NEG = ['not_south']
    ANNOTATIONS = ['talks more about discrimination','talks about economic struggles']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_parenting_subreddits_breastfeeding_baby_food():
    """Parenting reddit posts related to breastfeeding versus baby food."""

    DATASET = 'parenting_subreddits'
    POS = ['breastfeeding']
    NEG = ['baby food']
    ANNOTATIONS = ['talks more about breastfeeding','more frustrated']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_parenting_subreddits_single_non_biological_parents():
    """Parenting reddit posts related to single parents versus non-biological parents."""

    DATASET = 'parenting_subreddits'
    POS = ['sinle parents']
    NEG = ['non-biological parents']
    ANNOTATIONS = ['talks more about finances','talks less about connecting with children']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_parenting_subreddits_parent_support_interaction():
    """Parenting reddit posts related to parent support versus parent-child interaction."""

    DATASET = 'parenting_subreddits'
    POS = ['parent support']
    NEG = ['parent-child interaction']
    ANNOTATIONS = ['speaker is younger','talks more about the parent']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_rate_my_prof_female_male():
    """RateMyProfessor.com reviews for lecturers with generally male versus female names."""

    DATASET = 'rate_my_prof'
    POS = ['female']
    NEG = ['male']
    ANNOTATIONS = ['expresses more disatisfaction','comments on lecturing style','complains of being annoyed','claims that professor is unqualified']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_reddit_humor_funny_unfunny():
    """Funny versus unfunny jokes posted on r/jokes."""

    DATASET = 'reddit_humor'
    POS = ['funny']
    NEG = ['unfunny']
    ANNOTATIONS = ['is longer in length','has a surprising punchline','is not about race']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_reddit_stress_ptsd_anxiety():
    """Reddit posts related to PTSD versus anxiety."""

    DATASET = 'reddit_stress'
    POS = ['ptsd']
    NEG = ['anxiety']
    ANNOTATIONS = ['mentions military service','mentions trauma']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_reddit_stress_anxiety_stress():
    """Reddit posts related to anxiety versus stress."""

    DATASET = 'reddit_stress'
    POS = ['anxiety']
    NEG = ['stress']
    ANNOTATIONS = ['talks about the future','mentions social standing','talks more about depression']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_reuters_authorship_robinsidel_bernardhickey():
    """50 pieces from Reuters journalists Robin Sidel and Bernard Hickey, who both report financial news."""

    DATASET = 'reuters_authorship'
    POS = ['RobinSidel']
    NEG = ['BernardHickey']
    ANNOTATIONS = ['uses more quotes','contains longer sentences','talks about the stock market']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)


def pair_reuters_authorship_lynneodonnel_sarahdavison():
    """50 pieces from Reuters journalists Lynne O'Donnel and Sarah Davidson, who both write about China."""

    DATASET = 'reuters_authorship'
    POS = ["LynneO'Donnell"]
    NEG = ['SarahDavison']
    ANNOTATIONS = ['talks more about the economy','uses fewer quotations','expresses greater uncertainty']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_reuters_authorship_janlopatka_john_mastrini():
    """50 pieces from Reuters journalists Jan Lopatka and John Mastrini, who both write about the Czech Republic."""

    DATASET = 'reuters_authorship'
    POS = ["JanLopatka"]
    NEG = ['JohnMastrini']
    ANNOTATIONS = ['talks more about politics','talks less about the economy','expresses more political views']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_short_answer_scoring_good_bad():
    """Short answer responses with good versus (2.5+/3) bad scores (1/3)."""

    DATASET = 'short_answer_scoring'
    POS = ["good_answers"]
    NEG = ['bad_answers']
    ANNOTATIONS = ['uses correct grammar','gives more detail','is longer']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_short_answer_scoring_good_medium():
    """Short answer responses with good (2.5+/3) versus medium scores (1.5-2/3)."""

    DATASET = 'short_answer_scoring'
    POS = ["good_answers"]
    NEG = ['medium_answers']
    ANNOTATIONS = ['gives more examples','is longer']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_stock_news_up_down():
    """Reddit news headlines linked with whether the stock market went up or down that day."""

    DATASET = 'stock_news'
    POS = ["up"]
    NEG = ['down']
    ANNOTATIONS = ['talks about good news','talks about economic growth','more optimistic']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_suicide_notes_suicide_depression():
    """Reddit posts from depression vs. suicide related subreddits."""

    DATASET = 'suicide_notes'
    POS = ['suicide']
    NEG = ['depression']
    ANNOTATIONS = ['is more apologetic','mentions family and friends','is longer','uses better grammar']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_times_india_headlines_2003_2004():
    """Times of India news headlines from 2003 and 2004."""

    DATASET = 'times_india_headlines'
    POS = ['2003']
    NEG = ['2004']
    ANNOTATIONS = ['talks more about iraq','mentions train crashes','talks about Nadimarg massacre']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_times_india_headlines_2007_2008():
    """Times of India news headlines from 2007 and 2008."""

    DATASET = 'times_india_headlines'
    POS = ['2007']
    NEG = ['2008']
    ANNOTATIONS = ['talks less about the economy','is more optimistic']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def pair_times_india_headlines_2019_2020():
    """Times of India news headlines from 2019 and 2020."""

    DATASET = 'times_india_headlines'
    POS = ['2019']
    NEG = ['2020']
    ANNOTATIONS = ['does not mention COVID-19','is more optimistic']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def trial_deception_truth_lie():
    """Truths and lies told during real life trials."""

    DATASET = 'trial_deception'
    POS = ['truth']
    NEG = ['lie']
    ANNOTATIONS = ['admits to not knowing','does not claim innocence','longer sentences','expresses more uncertainty']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def tweet_gender_male_female():
    """Tweets from male versus female Twitter users."""

    DATASET = 'tweet_gender'
    POS = ['male_tweets']
    NEG = ['female_tweets']
    ANNOTATIONS = ['talks more about sports','talks more about politics','talks more about men']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def tweet_rumor_redhawks_early_late():
    """Early and late Twitter rumors about the 'Redhawks' name change."""

    DATASET = 'tweet_rumor'
    POS = ['redhawks_early']
    NEG = ['redhawks_late']
    ANNOTATIONS = ['is less skeptical','expresses more surprise']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def tweet_rumor_zucc_early_late():
    """Early and late Twitter rumors about Zuckerberg buying a yatch."""

    DATASET = 'tweet_rumor'
    POS = ['zuckerberg_yatch_early']
    NEG = ['zuckerberg_yatch_late']
    ANNOTATIONS = ['is less skeptical','expresses more surprise']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def tweet_rumor_denzel_wash_early_late():
    """Early and late Twitter rumors about Denzel Washington praising Trump."""

    DATASET = 'tweet_rumor'
    POS = ['denzel_washington_early']
    NEG = ['denzel_washington_late']
    ANNOTATIONS = ['is less skeptical','expresses more surprise']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def tweet_rumor_veggietales_early_late():
    """Early and late Twitter rumors about a new Veggietales cannabis character."""

    DATASET = 'tweet_rumor'
    POS = ['veggietales_early']
    NEG = ['veggietales_late']
    ANNOTATIONS = ['is less skeptical','expresses more surprise']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def twitter_misspellings_your_ur():
    """Tweets with and without an abbreviation of 'your' to 'ur'"""

    DATASET = 'twitter_misspellings'
    POS = ['your_misspell']
    NEG = ['your_proper']
    ANNOTATIONS = ['is part of a conversation','is more friendly']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def twitter_misspellings_with_wit():
    """Tweets with and without an abbreviation of 'with' to 'wit'"""

    DATASET = 'twitter_misspellings'
    POS = ['with_misspell']
    NEG = ['with_proper']
    ANNOTATIONS = ['is part of a conversation','is more friendly']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def twitter_misspellings_that_dat():
    """Tweets with and without an abbreviation of 'that' to 'dat'"""

    DATASET = 'twitter_misspellings'
    POS = ['that_misspell']
    NEG = ['that_proper']
    ANNOTATIONS = ['is part of a conversation','is more friendly']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def twitter_misspellings_going_goin():
    """Tweets with and without an abbreviation of 'going' to 'goin'"""

    DATASET = 'twitter_misspellings'
    POS = ['going_misspell']
    NEG = ['going_proper']
    ANNOTATIONS = ['is part of a conversation','is more friendly']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def unhealthy_conversations_dismissive_condescending():
    """Unhealthy conversations characterized as dismissive vs. condescending."""

    DATASET = 'unhealthy_conversations'
    POS = ['dismissive']
    NEG = ['condescending']
    ANNOTATIONS = ['is not insulting','is shorter']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def unhealthy_conversations_generalisation_unfair():
    """Unhealthy conversations characterized as generalisation (not unfair) vs. generalisation unfair."""

    DATASET = 'unhealthy_conversations'
    POS = ['generalisation']
    NEG = ['generalisation_unfair']
    ANNOTATIONS = ['is more objective','provides more reasoning']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

def unhealthy_conversations_hostile_antagonize():
    """Unhealthy conversations characterized as hostlie vs. antagonizing."""

    DATASET = 'unhealthy_conversations'
    POS = ['hostile']
    NEG = ['antagonize']
    ANNOTATIONS = ['is less insulting','uses more curse words']

    return generate_pair(DATASET, POS, NEG, ANNOTATIONS)

constructors = [
    pair_abc_headlines_2007_2008,
    pair_abc_headlines_2019_2020,
    pair_ad_transcripts_automative_travel,
    pair_ad_transcripts_beauty_care,
    pair_admin_statements_obama_biden,
    pair_admin_statements_trump_biden,
    pair_armenian_jobs_sw_qa,
    pair_armenian_jobs_junior_senior,
    pair_armenian_jobs_pre_post_recession,
    pair_armenian_jobs_reqs_pre_post_2012,
    pair_armenian_jobs_apps_pre_post_2012,
    pair_clickbait_headlines_pre_post_2013,
    pair_convincing_arguments_convincing_unconvincing,
    pair_dice_jobs_amazon_dell,
    pair_dice_jobs_northup_grumman_leidos,
    pair_dice_jobs_jpm_chase_deloitte,
    pair_diplomacy_deception_truth_lie,
    pair_drug_experiences_cocaine_molly,
    pair_drug_experiences_lsd_dxm,
    pair_drug_experiences_lsd_shrooms,
    pair_echr_decisions_yes_no_violation,
    pair_essay_scoring_good_bad,
    pair_fake_news_fake_legit,
    pair_fomc_speeches_greenspan_bernanke,
    pair_fomc_speeches_greenspan_bernanke_years,
    pair_fomc_speeches_yellen_powell_years,
    pair_fomc_speeches_unemployment,
    pair_fomc_speeches_growth,
    pair_fomc_speeches_interest_rate,
    pair_microedit_humor_unfunny_funny,
    pair_microedit_humor_funny_very_funny,
    pair_monster_jobs_atl_tampa,
    pair_monster_jobs_ca_tx,
    pair_monster_jobs_sf_nyc,
    pair_news_popularity_economy_pop_unpop,
    pair_news_popularity_microsoft_pop_unpop,
    pair_news_popularity_obama_pop_unpop,
    pair_news_popularity_obama_pos_neg,
    pair_npt_conferences_pre_post_2008,
    pair_npt_conferences_pre_post_2012,
    pair_open_deception_lie_truth,
    pair_open_review_good_bad,
    pair_open_review_great_good,
    pair_oral_histories_pre_post_1930,
    pair_oral_histories_pre_post_1950,
    pair_oral_histories_black_white,
    pair_oral_histories_asian_white,
    pair_oral_histories_college_educated,
    pair_oral_histories_south_not_south,
    pair_parenting_subreddits_breastfeeding_baby_food,
    pair_parenting_subreddits_single_non_biological_parents,
    pair_parenting_subreddits_parent_support_interaction,
    pair_rate_my_prof_female_male,
    pair_reddit_humor_funny_unfunny,
    pair_reddit_stress_ptsd_anxiety,
    pair_reddit_stress_anxiety_stress,
    pair_reuters_authorship_robinsidel_bernardhickey,
    pair_reuters_authorship_lynneodonnel_sarahdavison,
    pair_reuters_authorship_janlopatka_john_mastrini,
    pair_short_answer_scoring_good_bad,
    pair_short_answer_scoring_good_medium,
    pair_stock_news_up_down,
    pair_suicide_notes_suicide_depression,
    pair_times_india_headlines_2003_2004,
    pair_times_india_headlines_2007_2008,
    pair_times_india_headlines_2019_2020,
    trial_deception_truth_lie,
    tweet_gender_male_female,
    tweet_rumor_redhawks_early_late,
    tweet_rumor_zucc_early_late,
    tweet_rumor_denzel_wash_early_late,
    tweet_rumor_veggietales_early_late,
    twitter_misspellings_your_ur,
    twitter_misspellings_with_wit,
    twitter_misspellings_that_dat,
    twitter_misspellings_going_goin,
    unhealthy_conversations_dismissive_condescending,
    unhealthy_conversations_generalisation_unfair,
    unhealthy_conversations_hostile_antagonize,
]

def main():

    # pbar = tqdm(enumerate(constructors[:13]))
    pairs = []

    for i, constructor in enumerate(constructors):
        # pbar.set_description(f'processing pair {i}')
        new_pair = constructor()
        print('---')
        print(constructor.__name__)
        describe_pair(new_pair)
        pairs.append(new_pair)

    
    json.dump(pairs, open(PAIRS_FILE, 'w'))

if __name__ == '__main__':
    main()