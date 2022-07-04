from itertools import chain
import json
from typing import List

from tqdm import tqdm

from parameters import *

def generate_pair(
        pair: str, # name of the pair
        dataset: str, # name of the dataset
        pos_desc: str, # description of pos samples
        neg_desc: str, # description of neg samples
        pos: List[str], # positive samples
        neg: List[str], # negative samples
        annotations: List[str] # example annotations
        ): 
    """Creates pair of distributions and relevant metadata."""

    path = f'{OUTPUT_FOLDER}/{dataset}.json'
    output = json.load(open(path, 'r'))
    pos_dists = [output['data'][dist] for dist in pos]
    neg_dists = [output['data'][dist] for dist in neg]
    pos_samples = list(chain.from_iterable(pos_dists))
    neg_samples = list(chain.from_iterable(neg_dists))

    return {
        'pair':pair,
        'dataset':dataset,
        'human_annotations':annotations,
        'positive_description':pos_desc,
        'negative_description':neg_desc,
        'positive_samples':pos_samples,
        'negative_samples':neg_samples,
        'notes':''
    }

def describe_pair(pair):
    """Prints relevant information about dataset"""

    print('----')
    print('dataset:',pair['dataset'])
    print('# annotations:',len(pair['human_annotations']))
    print('# pos samples:',len(pair['positive_samples']))
    print('# neg samples:',len(pair['negative_samples']))

def pair_abc_headlines_2007_2008():
    """ABC news headlines from 2007 and 2008."""

    PAIR = 'abc_headlines_2007_2008'
    DATASET = 'abc_headlines'
    POS_DESC = 'ABC news headlines from 2007'
    NEG_DESC = 'ABC news headlines from 2008'
    POS = ['2007']
    NEG = ['2008']
    ANNOTATIONS = ['talks less about the economy']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_abc_headlines_2019_2020():
    """ABC news headlines from 2019 and 2020."""

    PAIR = 'abc_headlines_2019_2020'
    DATASET = 'abc_headlines'
    POS_DESC = 'ABC news headlines from 2019'
    NEG_DESC = 'ABC news headlines from 2020'
    POS = ['2019']
    NEG = ['2020']
    ANNOTATIONS = ['talks less about COVID-19', 'more positive']
    
    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_ad_transcripts_automative_travel():
    """Ad transcripts for automobile and travel companies."""

    PAIR = 'ad_transcripts_automative_travel'
    DATASET = 'ad_transcripts'
    POS_DESC = 'ad transcripts for automobile companies'
    NEG_DESC = 'ad transcripts for travel companies'
    POS = ['Automotive']
    NEG = ['Travel']
    ANNOTATIONS = ['talks more about performance','talks more about family']
    
    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_ad_transcripts_beauty_care():
    """Ad transcripts for beauty products and personal care products."""

    PAIR = 'ad_transcripts_beauty_care'
    DATASET = 'ad_transcripts'
    POS_DESC = 'ad transcripts for beauty products'
    NEG_DESC = 'ad transcripts for personal care products'
    POS = ['Beauty']
    NEG = ['Home & Personal Care']
    ANNOTATIONS = ['talks more about seeing','talks more about fashion']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_admin_statements_obama_biden():
    """Administration statements from Obama and Biden."""

    PAIR = 'admin_statements_obama_biden'
    DATASET = 'admin_statements'
    POS_DESC = 'administration statements from Obama'
    NEG_DESC = 'administration statements from Biden'
    POS = ['44-Obama']
    NEG = ['46-Biden']
    ANNOTATIONS = ['talks more about the economy', 'talks less about COVID-19']
    
    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_admin_statements_trump_biden():
    """Administration statements from Trump and Biden."""

    PAIR = 'admin_statements_trump_biden'
    DATASET = 'admin_statements'
    POS_DESC = 'administration statements from Trump'
    NEG_DESC = 'administration statements from Biden'
    POS = ['45-Trump']
    NEG = ['46-Biden']
    ANNOTATIONS = ['talks more about immigration', 'favor conservative policies', 'talks less about COVID-19']
    
    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_armenian_jobs_sw_qa():
    """Armenian job postings for software vs. QA positions."""

    PAIR = 'armenian_jobs_sw_qa'
    DATASET = 'armenian_jobs'
    POS_DESC = 'job postings for software positions'
    NEG_DESC = 'job postings for quality assurance positions'
    POS = ['job_desc_sw_dev','job_desc_senior_sw_dev','job_desc_sw_eng','job_desc_senior_sw_eng']
    NEG = ['job_desc_qa_eng','job_desc_senior_qa_eng']
    ANNOTATIONS = ['talks less about testing','talks more about development']
    
    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_armenian_jobs_junior_senior():
    """Armenian job postings for junior vs. senior positions."""

    PAIR = 'armenian_jobs_junior_senior'
    DATASET = 'armenian_jobs'
    POS_DESC = 'job postings for junior positions'
    NEG_DESC = 'job postings for senior positions'
    POS = ['job_req_senior_sw_dev','job_req_senior_sw_eng','job_req_senior_qa_eng']
    NEG = ['job_req_qa_eng','job_req_sw_eng','job_req_sw_dev',]
    ANNOTATIONS = ['reqiures more experience','talks about senior positions']
    
    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_armenian_jobs_pre_post_recession():
    """Armenian job postings for 2004-2006 and 2007-2009."""

    PAIR = 'armenian_jobs_pre_post_recession'
    DATASET = 'armenian_jobs'
    POS_DESC = 'job postings from 2004 to 2006'
    NEG_DESC = 'job postings from 2007 to 2009'
    POS = ['job_req_years_2004_2007']
    NEG = ['job_req_years_2007_2010',]
    ANNOTATIONS = ['requires more experience','talks less about technology']
    
    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_armenian_jobs_reqs_pre_post_2012():
    """Armenian job posting requirements for 2010-2012 and 2013-2014."""
    
    PAIR = 'armenian_jobs_reqs_pre_post_2012'
    DATASET = 'armenian_jobs'
    POS_DESC = 'job postings from 2010 to 2012'
    NEG_DESC = 'job postings from 2013 to 2014'
    POS = ['job_req_years_2010_2013']
    NEG = ['job_req_years_2013_2015',]
    ANNOTATIONS = ['requires newer programming languages','requires more education']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_armenian_jobs_apps_pre_post_2012():
    """Armenian job posting application process for 2010-2012 and 2013-2014."""

    PAIR = 'armenian_jobs_apps_pre_post_2012'
    DATASET = 'armenian_jobs'
    POS_DESC = 'job applications processes from 2010 to 2012'
    NEG_DESC = 'job applications processes from 2013 to 2014'
    POS = ['app_process_years_2010_2013']
    NEG = ['app_process_years_2013_2015',]
    ANNOTATIONS = ['talks more about online applications']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_clickbait_headlines_pre_post_2013():
    """Clickbait headlines from the Examiner for 2010-2012 versus 2013-2015."""

    PAIR = 'clickbait_headlines_pre_post_2013'
    DATASET = 'clickbait_headlines'
    POS_DESC = 'clickbait headlines from 2010 to 2012'
    NEG_DESC = 'clickbait headlines from 2013 to 2015'
    POS = ['2010','2011','2012']
    NEG = ['2013','2014','2015']
    ANNOTATIONS = ['talks more about Mitt Romney']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_convincing_arguments_convincing_unconvincing():
    """Arguments in online forums rated convincing and unconvincing."""

    PAIR = 'convincing_arguments_convincing_unconvincing'
    DATASET = 'convincing_arguments'
    POS_DESC = 'convincing arguments'
    NEG_DESC = 'unconvincing arguments'
    POS = ['convincing']
    NEG = ['unconvincing']
    ANNOTATIONS = ['provides more explanation','gives examples','does not insult others']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_dice_jobs_amazon_dell():
    """Job postings on Dice from Amazon vs. Dell."""

    PAIR = 'dice_jobs_amazon_dell'
    DATASET = 'dice_jobs'
    POS_DESC = 'job postings for Amazon'
    NEG_DESC = 'job postings for Dell'
    POS = ['amazon']
    NEG = ['dell']
    ANNOTATIONS = ['talks more about Java','talks more about software']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_dice_jobs_northup_grumman_leidos():
    """Job postings on Dice from Northup Grumman vs. Leidos."""

    PAIR = 'dice_jobs_northup_grumman_leidos'
    DATASET = 'dice_jobs'
    POS_DESC = 'job postings for Northup Grumman'
    NEG_DESC = 'job postings for Leidos'
    POS = ['northup_grumman']
    NEG = ['leidos']
    ANNOTATIONS = ['talks more about aerospace']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_dice_jobs_jpm_chase_deloitte():
    """Job postings on Dice from JP Morgan Chase vs. Deloitte."""

    PAIR = 'dice_jobs_jpm_chase_deloitte'
    DATASET = 'dice_jobs'
    POS_DESC = 'job postings for JP Morgan Chase'
    NEG_DESC = 'job postings for Deloitte'
    POS = ['jpm']
    NEG = ['deloitte']
    ANNOTATIONS = ['talks more about banking','talks less about consulting']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_diplomacy_deception_truth_lie():
    """True and false statements during games of Diplomacy."""

    PAIR = 'diplomacy_deception_truth_lie'
    DATASET = 'diplomacy_deception'
    POS_DESC = 'true statements in a game'
    NEG_DESC = 'deceptive statements in a game'
    POS = ['truth']
    NEG = ['lie']
    ANNOTATIONS = ['makes fewer requests','praises the other player less']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_drug_experiences_cocaine_molly():
    """Self-reported experiences of users of cocaine and MDMA."""

    PAIR = 'drug_experiences_cocaine_molly'
    DATASET = 'drug_experiences'
    POS_DESC = 'accounts of cocaine use'
    NEG_DESC = 'accounts of MDMA use'
    POS = ['cocaine']
    NEG = ['mdma']
    ANNOTATIONS = ['talks more about hallucinations','talks about concerts']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_drug_experiences_lsd_dxm():
    """Self-reported experiences of users of LSD and dextromethorphan (DXM)."""

    PAIR = 'drug_experiences_lsd_dxm'
    DATASET = 'drug_experiences'
    POS_DESC = 'accounts of LSD use'
    NEG_DESC = 'accounts of DXM use'
    POS = ['lsd']
    NEG = ['dxm']
    ANNOTATIONS = ['more realistic experiences','talks more about visions']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_drug_experiences_lsd_shrooms():
    """Self-reported experiences of users of LSD and mushrooms."""

    PAIR = 'drug_experiences_lsd_shrooms'
    DATASET = 'drug_experiences'
    POS_DESC = 'accounts of LSD use'
    NEG_DESC = 'accounts of mushroom use'
    POS = ['lsd']
    NEG = ['mushrooms']
    ANNOTATIONS = ['talks about higher energy','mentions fewer hallucinations']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_echr_decisions_yes_no_violation():
    """ECHR rulings that did or did not find a violation of an article."""

    PAIR = 'echr_decisions_yes_no_violation'
    DATASET = 'echr_decisions'
    POS_DESC = 'human rights trials where a violation was found'
    NEG_DESC = 'human rights trials where no violation was found'
    POS = ['violation']
    NEG = ['no_violation']
    ANNOTATIONS = ['talks more about witnesses','mentions more violence']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_essay_scoring_good_bad():
    """Essays on the same topic with good or bad scores."""

    PAIR = 'essay_scoring_good_bad'
    DATASET = 'essay_scoring'
    POS_DESC = 'essays with good scores'
    NEG_DESC = 'essays with bad scores'
    POS = ['good_essays']
    NEG = ['bad_essays']
    ANNOTATIONS = ['has longer sentences','uses longer words','has more words','is more coherent','has fewer spelling mistakes']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_fake_news_fake_legit():
    """News articles that are either fake or legit."""

    PAIR = 'fake_news_fake_legit'
    DATASET = 'fake_news'
    POS_DESC = 'fake news articles'
    NEG_DESC = 'legitimate news articles'
    POS = ['fake']
    NEG = ['legit']
    ANNOTATIONS = ['uses more extreme language','cites fewer sources','is more political']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_fomc_speeches_greenspan_bernanke():
    """FOMC speeches from Chairman Greenspan and Chairman Bernanke."""

    PAIR = 'fomc_speeches_greenspan_bernanke'
    DATASET = 'fomc_speeches'
    POS_DESC = 'FOMC speeches from Chairman Greenspan'
    NEG_DESC = 'FOMC speeches from Chairman Bernanke'
    POS = ['greenspan_speeches']
    NEG = ['bernanke_speeches']
    ANNOTATIONS = ['calls for more action','talks more about growth','talks less about targets']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_fomc_speeches_greenspan_bernanke_years():
    """FOMC speeches from the terms of Chariman Greenspan (-2006) and Chairman Bernanke (2006-2014)."""

    PAIR = 'fomc_speeches_greenspan_bernanke_year'
    DATASET = 'fomc_speeches'
    POS_DESC = 'FOMC speeches from before 2006'
    NEG_DESC = 'FOMC speeches from 2006 to 2014'
    POS = ['greenspan_years']
    NEG = ['bernanke_years']
    ANNOTATIONS = ['calls for more action','talks more about growth','talks less about targets']
    
    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_fomc_speeches_yellen_powell_years():
    """FOMC speeches from the terms of Chariman Yellen (2014-2018) and Chairman Powell (2018-)."""

    PAIR = 'fomc_speeches_yellen_powell_years'
    DATASET = 'fomc_speeches'
    POS_DESC = 'FOMC speeches from 2014 to 2018'
    NEG_DESC = 'FOMC speeches from after 2018'
    POS = ['yellen_years']
    NEG = ['powell_years']
    ANNOTATIONS = ['talks more about unemployment','does not mention COVID-19','talks about economic growth']
    
    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_fomc_speeches_unemployment():
    """FOMC speeches during periods of high and low unemployment."""

    PAIR = 'fomc_speeches_unemployment'
    DATASET = 'fomc_speeches'
    POS_DESC = 'FOMC speeches during periods of high unemployment'
    NEG_DESC = 'FOMC speeches during periods of low unemployment'
    POS = ['high_unemp']
    NEG = ['low_unemp']
    ANNOTATIONS = ['talks more about unemployment','talks about lowering the interest rate','talks less about inflation']
    
    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_fomc_speeches_growth():
    """FOMC speeches during periods of high and low GDP growth."""

    PAIR = 'fomc_speeches_growth'
    DATASET = 'fomc_speeches'
    POS_DESC = 'FOMC speeches during periods of high GDP growth'
    NEG_DESC = 'FOMC speeches during periods of low GDP growth'
    POS = ['high_growth']
    NEG = ['low_growth']
    ANNOTATIONS = ['talks more about inflation','is more optimistic']
    
    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_fomc_speeches_interest_rate():
    """FOMC speeches during periods of high and low fed interest rate."""

    PAIR = 'fomc_speeches_interest_rate'
    DATASET = 'fomc_speeches'
    POS_DESC = 'FOMC speeches during periods of high interest rates'
    NEG_DESC = 'FOMC speeches during periods of low interest rates'
    POS = ['high_ir']
    NEG = ['low_ir']
    ANNOTATIONS = ['talks more about inflation','worries more about recession']
    
    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_microedit_humor_unfunny_funny():
    """Humor generated from microedits that are either unfunny or funny."""

    PAIR = 'microedit_humor_unfunny_funny'
    DATASET = 'microedit_humor'
    POS_DESC = 'edited sentences that are not funny'
    NEG_DESC = 'edited sentences that are funny'
    POS = ['unfunny']
    NEG = ['funny']
    ANNOTATIONS = ['is incoherent','is expected']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_happy_moments_affection_bonding():
    """Happy moments about affection vs. bonding."""

    PAIR = 'happy_moments_affection_bonding'
    DATASET = 'happy_moments'
    POS_DESC = 'happy moments about affection'
    NEG_DESC = 'happy moments about bonding'
    POS = ['affection']
    NEG = ['bonding']
    ANNOTATIONS = ['talks more about relatives', 'talk more about love']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_happy_moments_enjoying_leisure():
    """Happy moments about enjoying the moment vs. leisure."""

    PAIR = 'happy_moments_enjoying_leisure'
    DATASET = 'happy_moments'
    POS_DESC = 'happy moments about enjoying the moment'
    NEG_DESC = 'happy moments about leisure'
    POS = ['enjoy_the_moment']
    NEG = ['leisure']
    ANNOTATIONS = ['talks more about experiences','talks less about relaxing','does not mention vacation']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_happy_moments_usa_india():
    """Happy moments from the United States vs. India."""

    PAIR = 'happy_moments_usa_india'
    DATASET = 'happy_moments'
    POS_DESC = 'happy moments from the United States'
    NEG_DESC = 'happy moments from India'
    POS = ['usa']
    NEG = ['india']
    ANNOTATIONS = ['talks about friends','talks about leisure','talks less about others']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_happy_moments_usa_venezuela():
    """Happy moments from the United States vs. Venezuela."""

    PAIR = 'happy_moments_usa_venezuela'
    DATASET = 'happy_moments'
    POS_DESC = 'happy moments from the United States'
    NEG_DESC = 'happy moments from Venezuela'
    POS = ['usa']
    NEG = ['venezuela']
    ANNOTATIONS = ['talks about friends','talks about leisure','talks less about others']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_happy_moments_usa_canada():
    """Happy moments from the United States vs. Canada."""

    PAIR = 'happy_moments_usa_canada'
    DATASET = 'happy_moments'
    POS_DESC = 'happy moments from the United States'
    NEG_DESC = 'happy moments from Canada'
    POS = ['usa']
    NEG = ['canada']
    ANNOTATIONS = ['talks about friends','talks less about nature','talks more about consumption']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_happy_moments_college_20s():
    """Happy moments from 18-21 year olds versus 22-25 year olds."""

    PAIR = 'happy_moments_college_20s'
    DATASET = 'happy_moments'
    POS_DESC = 'happy moments from 18-21 year olds'
    NEG_DESC = 'happy moments from 22-25 year olds'
    POS = ['18-21']
    NEG = ['22-25']
    ANNOTATIONS = ['talks about traveling','talks about new places','talks about relationships']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_happy_moments_early_late_20s():
    """Happy moments from 22-25 year olds versus 26-35 year olds."""

    PAIR = 'happy_moments_early_late_20s'
    DATASET = 'happy_moments'
    POS_DESC = 'happy moments from 22-25 year olds'
    NEG_DESC = 'happy moments from 26-35 year olds'
    POS = ['22-25']
    NEG = ['26-35']
    ANNOTATIONS = ['talks about traveling','talks about new places']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)


def pair_happy_moments_30s_40s():
    """Happy moments from 36-45 year olds versus 46+ year olds."""

    PAIR = 'happy_moments_30s_40s'
    DATASET = 'happy_moments'
    POS_DESC = 'happy moments from 36-45 year olds'
    NEG_DESC = 'happy moments from 46+ year olds'
    POS = ['36-45']
    NEG = ['46+']
    ANNOTATIONS = ['talks about children','talks more about work']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_happy_moments_gender():
    """Happy moments from men and women."""

    PAIR = 'happy_moments_gender'
    DATASET = 'happy_moments'
    POS_DESC = 'happy moments from males'
    NEG_DESC = 'happy moments from females'
    POS = ['male']
    NEG = ['female']
    ANNOTATIONS = ['talks about work','talks about friends']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_happy_moments_parenthood():
    """Happy moments from those with and without children."""

    PAIR = 'happy_moments_parenthood'
    DATASET = 'happy_moments'
    POS_DESC = 'happy moments from parents'
    NEG_DESC = 'happy moments from non-parents'
    POS = ['parent']
    NEG = ['not_parent']
    ANNOTATIONS = ['talks about children','talks about spouses']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_happy_moments_marraige():
    """Happy moments from those who are and aren't married."""

    PAIR = 'happy_moments_marraige'
    DATASET = 'happy_moments'
    POS_DESC = 'happy moments from married people'
    NEG_DESC = 'happy moments from single people'
    POS = ['single']
    NEG = ['married']
    ANNOTATIONS = ['talks about dating','talks about relatives']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_happy_moments_separation_divorce():
    """Happy moments from those who are separated vs. divorced."""

    PAIR = 'happy_moments_separation_divorce'
    DATASET = 'happy_moments'
    POS_DESC = 'happy moments from separated people'
    NEG_DESC = 'happy moments from divorced people'
    POS = ['separated']
    NEG = ['divorced']
    ANNOTATIONS = ['talks about children','talks about relatives']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_microedit_humor_funny_very_funny():
    """Humor generated from microedits that are funny or very funny."""

    PAIR = 'microedit_humor_funny_very_funny'
    DATASET = 'microedit_humor'
    POS_DESC = 'edited sentences that are somewhat funny'
    NEG_DESC = 'edited sentences that are very funny'
    POS = ['funny']
    NEG = ['very_funny']
    ANNOTATIONS = ['is less surprising','uses slapstick humor']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)


def pair_monster_jobs_atl_tampa():
    """Job postings on Monster.com in Atlanta, GA vs. Tampa, FL."""

    PAIR = 'monster_jobs_atl_tampa'
    DATASET = 'monster_jobs'
    POS_DESC = 'job postings for Atlanta, GA'
    NEG_DESC = 'job postings for Tampa, FL'
    POS = ['atlanta']
    NEG = ['tampa']
    ANNOTATIONS = ['offers blue collar jobs','talks less about the beach']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_monster_jobs_ca_tx():
    """Job postings on Monster.com in California versus Texas."""

    PAIR = 'monster_jobs_ca_tx'
    DATASET = 'monster_jobs'
    POS_DESC = 'job postings in California'
    NEG_DESC = 'job postings in Texas'
    POS = ['sf','la','berkeley']
    NEG = ['dallas','houston','austin']
    ANNOTATIONS = ['offers tech related jobs','offers more benefits','offers greater compensation']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_monster_jobs_sf_nyc():
    """Job postings on Monster.com in NYC versus San Francisco."""

    PAIR = 'monster_jobs_sf_nyc'
    DATASET = 'monster_jobs'
    POS_DESC = 'job postings in New York City'
    NEG_DESC = 'job postings in San Francisco'
    POS = ['nyc']
    NEG = ['sf']
    ANNOTATIONS = ['offers more finance jobs','talks more about location']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_movie_popularity_hit_average():
    """Hit movies versus average movies"""

    PAIR = 'movie_popularity_hit_average'
    DATASET = 'movie_popularity'
    POS_DESC = 'descriptions of very popular movies'
    NEG_DESC = 'descriptions of average movies'
    POS = ['hit']
    NEG = ['average']
    ANNOTATIONS = ['mentions a superhero','talks more about surprise']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_movie_popularity_bad_average():
    """Bad movies versus average movies"""

    PAIR = 'movie_popularity_bad_average'
    DATASET = 'movie_popularity'
    POS_DESC = 'descriptions of bad movies'
    NEG_DESC = 'descriptions of average movies'
    POS = ['bad']
    NEG = ['average']
    ANNOTATIONS = ['is a documentary','is a remake']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_news_popularity_economy_pop_unpop():
    """Popular vs. unpoplar Bloomberg news related to the economy, measured by Facebook engagement."""

    PAIR = 'news_popularity_economy_pop_unpop'
    DATASET = 'news_popularity'
    POS_DESC = 'popular articles about the economy'
    NEG_DESC = 'unpopular articles about the economy'
    POS = ['economy_pop']
    NEG = ['economy_unpop']
    ANNOTATIONS = ['is about an economic shock','talks about the U.S. economy']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_news_popularity_microsoft_pop_unpop():
    """Popular vs. unpoplar Bloomberg news related to Microsoft, measured by Facebook engagement."""

    PAIR = 'news_popularity_microsoft_pop_unpop'
    DATASET = 'news_popularity'
    POS_DESC = 'popular articles about Microsoft'
    NEG_DESC = 'unpopular articles about Microsoft'
    POS = ['microsoft_pop']
    NEG = ['microsoft_unpop']
    ANNOTATIONS = ['talks about user privacy','talks about Zuckerberg']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_news_popularity_obama_pop_unpop():
    """Popular vs. unpoplar Bloomberg news related to Obama, measured by Facebook engagement."""

    PAIR = 'news_popularity_obama_pop_unpop'
    DATASET = 'news_popularity'
    POS_DESC = 'popular articles about Obama'
    NEG_DESC = 'unpopular articles about Obama'
    POS = ['obama_pop']
    NEG = ['obama_unpop']
    ANNOTATIONS = ['talks about Obama negatively','talks about Afghanistan']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)
    
def pair_news_popularity_obama_pos_neg():
    """Positive or negative sentiment news related to Obama."""

    PAIR = 'news_popularity_obama_pos_neg'
    DATASET = 'news_popularity'
    POS_DESC = 'positive articles about Obama'
    NEG_DESC = 'negative articles about Obama'
    POS = ['obama_pos']
    NEG = ['obama_neg']
    ANNOTATIONS = ['talks about Obamacare','talks about the economy']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_npt_conferences_pre_post_2008():
    """NPT conference reports from before 2008 and between 2008-2012."""

    PAIR = 'npt_conferences_pre_post_2008'
    DATASET = 'npt_conferences'
    POS_DESC = 'NPT conference reports before 2008'
    NEG_DESC = 'NPT conference reports between 2008 and 2012'
    POS = ['pre_2008']
    NEG = ['btw_2008_2012']
    ANNOTATIONS = ['mentions Iran','mentions 9/11','talks less about the economy']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_npt_conferences_pre_post_2012():
    """NPT conference reports from between 2008-2012 and after 2012."""

    PAIR = 'npt_conferences_pre_post_2012'
    DATASET = 'npt_conferences'
    POS_DESC = 'NPT conference reports between 2008 and 2012'
    NEG_DESC = 'NPT conference reports after 2012'
    POS = ['btw_2008_2012']
    NEG = ['post_2012']
    ANNOTATIONS = ['mentions Russia','talks about hypersonic missiles']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_open_deception_lie_truth():
    """Human generated truths and lies from any domain."""

    PAIR = 'open_deception_lie_truth'
    DATASET = 'open_deception'
    POS_DESC = 'random truth statements'
    NEG_DESC = 'random false statements'
    POS = ['lie']
    NEG = ['truth']
    ANNOTATIONS = ['talks about themselves','uses extreme adjectives']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_open_review_good_bad():
    """Open Review papers that recieved good (5-7) ratings versus bad (<5)."""

    PAIR = 'open_review_good_bad'
    DATASET = 'open_review'
    POS_DESC = 'good journal submissions'
    NEG_DESC = 'bad journal submissions'
    POS = ['good_papers']
    NEG = ['bad_papers']
    ANNOTATIONS = ['is better written','provides more equations']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_open_review_great_good():
    """Open Review papers that recieved great (8+) versus good (5-7) ratings."""

    PAIR = 'open_review_great_good'
    DATASET = 'open_review'
    POS_DESC = 'good journal submissions'
    NEG_DESC = 'very good journal submissions'
    POS = ['great_papers']
    NEG = ['good_papers']
    ANNOTATIONS = ['expresses surprise','introduces a benchmark','introduces a new technique']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_oral_histories_pre_post_1930():
    """Oral histories from people born pre-1930 versus 1930-1950."""

    PAIR = 'oral_histories_pre_post_1930'
    DATASET = 'oral_histories'
    POS_DESC = 'oral histories of people born before 1930'
    NEG_DESC = 'oral histories of people born between 1930 and 1950'
    POS = ['pre_1930']
    NEG = ['1930-50']
    ANNOTATIONS = ['talks more about racism','talks about older presidents','mentions World War I']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_oral_histories_pre_post_1950():
    """Oral histories from people born 1930-1950 versus post-1950."""

    PAIR = 'oral_histories_pre_post_1950'
    DATASET = 'oral_histories'
    POS_DESC = 'oral histories of people born between 1930 and 1950'
    NEG_DESC = 'oral histories of people born after 1950'
    POS = ['1930-50']
    NEG = ['post_1950']
    ANNOTATIONS = ['talks about the Great Depression','mentions World War II']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)
    
def pair_oral_histories_black_white():
    """Oral histories from black versus white people."""

    PAIR = 'oral_histories_black_white'
    DATASET = 'oral_histories'
    POS_DESC = 'oral histories of black people'
    NEG_DESC = 'oral histories of white people'
    POS = ['black']
    NEG = ['white']
    ANNOTATIONS = ['talks more about racism','talks more about civil rights','discusses more violence']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_oral_histories_asian_white():
    """Oral histories from Asian versus white people."""

    PAIR = 'oral_histories_asian_white'
    DATASET = 'oral_histories'
    POS_DESC = 'oral histories of Asian people'
    NEG_DESC = 'oral histories of white people'
    POS = ['asian']
    NEG = ['white']
    ANNOTATIONS = ['talks more about racism','talks more about civil rights','discusses more violence']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_oral_histories_college_educated():
    """Oral histories from college-educated and non-college-educated people."""

    PAIR = 'oral_histories_college_educated'
    DATASET = 'oral_histories'
    POS_DESC = 'oral histories of people with college degrees'
    NEG_DESC = 'oral histories of people without college degrees'
    POS = ['college_educated']
    NEG = ['not_college_educated']
    ANNOTATIONS = ['talks more about academic jobs','mentions civil rights','uses eloquent language']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_oral_histories_south_not_south():
    """Oral histories from people born in the South versus elsewhere."""

    PAIR = 'oral_histories_south_not_south'
    DATASET = 'oral_histories'
    POS_DESC = 'oral histories of people from the South'
    NEG_DESC = 'oral histories of people not from the South'
    POS = ['south']
    NEG = ['not_south']
    ANNOTATIONS = ['talks more about discrimination','talks about economic struggles']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_parenting_subreddits_breastfeeding_baby_food():
    """Parenting reddit posts related to breastfeeding versus baby food."""

    PAIR = 'parenting_subreddits_breastfeeding_baby_food'
    DATASET = 'parenting_subreddits'
    POS_DESC = 'Reddit posts about breastfeeding'
    NEG_DESC = 'Reddit posts about baby food'
    POS = ['breastfeeding']
    NEG = ['baby food']
    ANNOTATIONS = ['talks more about breastfeeding','more frustrated']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_parenting_subreddits_single_non_biological_parents():
    """Parenting reddit posts related to single parents versus non-biological parents."""

    PAIR = 'parenting_subreddits_single_non_biological_parents'
    DATASET = 'parenting_subreddits'
    POS_DESC = 'Reddit posts from single parents'
    NEG_DESC = 'Reddit posts from non-biological parents'
    POS = ['sinle parents']
    NEG = ['non-biological parents']
    ANNOTATIONS = ['talks more about finances','talks less about connecting with children']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_parenting_subreddits_parent_support_interaction():
    """Parenting reddit posts related to parent support versus parent-child interaction."""

    PAIR = 'parenting_subreddits_parent_support_interaction'
    DATASET = 'parenting_subreddits'
    POS_DESC = 'Reddit posts from parents asking for support'
    NEG_DESC = 'Reddit posts from parents about interacting with children'
    POS = ['parent support']
    NEG = ['parent-child interaction']
    ANNOTATIONS = ['speaker is younger','talks more about the parent']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_rate_my_prof_female_male():
    """RateMyProfessor.com reviews for lecturers with generally male versus female names."""

    PAIR = 'rate_my_prof_female_male'
    DATASET = 'rate_my_prof'
    POS_DESC = 'RateMyProfessor.com reviews for female lecturers'
    NEG_DESC = 'RateMyProfessor.com reviews for male lecturers'
    POS = ['female']
    NEG = ['male']
    ANNOTATIONS = ['expresses more disatisfaction','comments on lecturing style','complains of being annoyed','claims that professor is unqualified']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_reddit_humor_funny_unfunny():
    """Funny versus unfunny jokes posted on r/jokes."""

    PAIR = 'reddit_humor_funny_unfunny'
    DATASET = 'reddit_humor'
    POS_DESC = 'funny Reddit jokes'
    NEG_DESC = 'unfunny Reddit jokes'
    POS = ['funny']
    NEG = ['unfunny']
    ANNOTATIONS = ['is longer in length','has a surprising punchline','is not about race']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_reddit_stress_ptsd_anxiety():
    """Reddit posts related to PTSD versus anxiety."""

    PAIR = 'reddit_stress_ptsd_anxiety'
    DATASET = 'reddit_stress'
    POS_DESC = 'posts from people with PTSD'
    NEG_DESC = 'posts from people with anxiety'
    POS = ['ptsd']
    NEG = ['anxiety']
    ANNOTATIONS = ['mentions military service','mentions trauma']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_reddit_stress_anxiety_stress():
    """Reddit posts related to anxiety versus stress."""

    PAIR = 'reddit_stress_anxiety_stress'
    DATASET = 'reddit_stress'
    POS_DESC = 'posts from people with anxiety'
    NEG_DESC = 'posts from people who are stressed'
    POS = ['anxiety']
    NEG = ['stress']
    ANNOTATIONS = ['talks about the future','mentions social standing','talks more about depression']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_reuters_authorship_robinsidel_bernardhickey():
    """50 pieces from Reuters journalists Robin Sidel and Bernard Hickey, who both report financial news."""

    PAIR = 'reuters_authorship_robinsidel_bernardhickey'
    DATASET = 'reuters_authorship'
    POS_DESC = 'news articles by Robin Sidel'
    NEG_DESC ='news articles by Bernard Hickey'
    POS = ['RobinSidel']
    NEG = ['BernardHickey']
    ANNOTATIONS = ['uses more quotes','contains longer sentences','talks about the stock market']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)


def pair_reuters_authorship_lynneodonnel_sarahdavison():
    """50 pieces from Reuters journalists Lynne O'Donnel and Sarah Davidson, who both write about China."""

    PAIR = 'reuters_authorship_lynneodonnel_sarahdavison'
    DATASET = 'reuters_authorship'
    POS_DESC = 'news articles by Lynne O\'Donnel'
    NEG_DESC ='news articles by Sarah Davidson'
    POS = ["LynneO'Donnell"]
    NEG = ['SarahDavison']
    ANNOTATIONS = ['talks more about the economy','uses fewer quotations','expresses greater uncertainty']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_reuters_authorship_janlopatka_john_mastrini():
    """50 pieces from Reuters journalists Jan Lopatka and John Mastrini, who both write about the Czech Republic."""

    PAIR = 'reuters_authorship_janlopatka_john_mastrini'
    DATASET = 'reuters_authorship'
    POS_DESC = 'news articles by Jan Lopatka'
    NEG_DESC ='news articles by John Mastrini'
    POS = ["JanLopatka"]
    NEG = ['JohnMastrini']
    ANNOTATIONS = ['talks more about politics','talks less about the economy','expresses more political views']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_short_answer_scoring_good_bad():
    """Short answer responses with good versus (2.5+/3) bad scores (1/3)."""

    PAIR = 'short_answer_scoring_good_bad'
    DATASET = 'short_answer_scoring'
    POS_DESC = 'good short answers'
    NEG_DESC ='bad short answers'
    POS = ["good_answers"]
    NEG = ['bad_answers']
    ANNOTATIONS = ['uses correct grammar','gives more detail','is longer']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_short_answer_scoring_good_medium():
    """Short answer responses with good (2.5+/3) versus medium scores (1.5-2/3)."""

    PAIR = 'short_answer_scoring_good_medium'
    DATASET = 'short_answer_scoring'
    POS_DESC = 'good short answers'
    NEG_DESC ='average short answers'
    POS = ["good_answers"]
    NEG = ['medium_answers']
    ANNOTATIONS = ['gives more examples','is longer']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_stock_news_up_down():
    """Reddit news headlines linked with whether the stock market went up or down that day."""

    PAIR = 'stock_news_up_down'
    DATASET = 'stock_news'
    POS_DESC = 'headlines on days the stock market rises'
    NEG_DESC ='headlines on days the stock market falls'
    POS = ["up"]
    NEG = ['down']
    ANNOTATIONS = ['talks about good news','talks about economic growth','more optimistic']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_suicide_notes_suicide_depression():
    """Reddit posts from depression vs. suicide related subreddits."""

    PAIR = 'suicide_notes_suicide_depression'
    DATASET = 'suicide_notes'
    POS_DESC = 'notes from people who committed suicide'
    NEG_DESC = 'notes from people who are depressed, but did not commit suicide'
    POS = ['suicide']
    NEG = ['depression']
    ANNOTATIONS = ['is more apologetic','mentions family and friends','is longer','uses better grammar']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_times_india_headlines_2003_2004():
    """Times of India news headlines from 2003 and 2004."""

    PAIR = 'times_india_headlines_2003_2004'
    DATASET = 'times_india_headlines'
    POS_DESC = 'Indian news headlines from 2003'
    NEG_DESC = 'Indian news headlines from 2004'
    POS = ['2003']
    NEG = ['2004']
    ANNOTATIONS = ['talks more about iraq','mentions train crashes','talks about Nadimarg massacre']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_times_india_headlines_2007_2008():
    """Times of India news headlines from 2007 and 2008."""

    PAIR = 'times_india_headlines_2007_2008'
    DATASET = 'times_india_headlines'
    POS_DESC = 'Indian news headlines from 2007'
    NEG_DESC = 'Indian news headlines from 2008'
    POS = ['2007']
    NEG = ['2008']
    ANNOTATIONS = ['talks less about the economy','is more optimistic']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_times_india_headlines_2019_2020():
    """Times of India news headlines from 2019 and 2020."""

    PAIR = 'times_india_headlines_2019_2020'
    DATASET = 'times_india_headlines'
    POS_DESC = 'Indian news headlines from 2019'
    NEG_DESC = 'Indian news headlines from 2020'
    POS = ['2019']
    NEG = ['2020']
    ANNOTATIONS = ['does not mention COVID-19','is more optimistic']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_trial_deception_truth_lie():
    """Truths and lies told during real life trials."""

    PAIR = 'trial_deception_truth_lie'
    DATASET = 'trial_deception'
    POS_DESC = 'truthful testimony in criminal trials'
    NEG_DESC = 'deceptive testimony in criminal trials'
    POS = ['truth']
    NEG = ['lie']
    ANNOTATIONS = ['admits to not knowing','does not claim innocence','longer sentences','expresses more uncertainty']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_tweet_gender_male_female():
    """Tweets from male versus female Twitter users."""

    PAIR = 'tweet_gender_male_female'
    DATASET = 'tweet_gender'
    POS_DESC = 'Tweets from male users'
    NEG_DESC = 'Tweets from female users'
    POS = ['male_tweets']
    NEG = ['female_tweets']
    ANNOTATIONS = ['talks more about sports','talks more about politics','talks more about men']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_tweet_rumor_redhawks_early_late():
    """Early and late Twitter rumors about the 'Redhawks' name change."""

    PAIR = 'tweet_rumor_redhawks_early_late'
    DATASET = 'tweet_rumor'
    POS_DESC = 'early Twitter rumors about the Redhawks'
    NEG_DESC = 'later Twitter rumors about the Redhawks'
    POS = ['redhawks_early']
    NEG = ['redhawks_late']
    ANNOTATIONS = ['is less skeptical','expresses more surprise']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_tweet_rumor_zucc_early_late():
    """Early and late Twitter rumors about Zuckerberg buying a yatch."""

    PAIR = 'tweet_rumor_zucc_early_late'
    DATASET = 'tweet_rumor'
    POS_DESC = 'early Twitter rumors about Zuckerberg buying a yatch'
    NEG_DESC = 'later Twitter rumors about Zuckerberg buying a yatch'
    POS = ['zuckerberg_yatch_early']
    NEG = ['zuckerberg_yatch_late']
    ANNOTATIONS = ['is less skeptical','expresses more surprise']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_tweet_rumor_denzel_wash_early_late():
    """Early and late Twitter rumors about Denzel Washington praising Trump."""

    PAIR = 'tweet_rumor_denzel_wash_early_late'
    DATASET = 'tweet_rumor'
    POS_DESC = 'early Twitter rumors about Denzel Washington praising Trump'
    NEG_DESC = 'later Twitter rumors about Denzel Washington praising Trump'
    POS = ['denzel_washington_early']
    NEG = ['denzel_washington_late']
    ANNOTATIONS = ['is less skeptical','expresses more surprise']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_tweet_rumor_veggietales_early_late():
    """Early and late Twitter rumors about a new Veggietales cannabis character."""

    PAIR = 'tweet_rumor_veggietales_early_late'
    DATASET = 'tweet_rumor'
    POS_DESC = 'early Twitter rumors about a Veggietales cannabis character'
    NEG_DESC = 'later Twitter rumors about a Veggietales cannabis character'
    POS = ['veggietales_early']
    NEG = ['veggietales_late']
    ANNOTATIONS = ['is less skeptical','expresses more surprise']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_twitter_bots_human():
    """Tweets from bots vs. humans."""

    PAIR = 'twitter_bots_human'
    DATASET = 'twitter_bots'
    POS_DESC = 'Tweets from bots'
    NEG_DESC = 'Tweets from humans'
    POS = ['trad_bot']
    NEG = ['human']
    ANNOTATIONS = ['talks about sexual topics','discusses politics','is negative']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_twitter_bots_trad_social():
    """Tweets from traditional bots vs. new social bots."""

    PAIR = 'twitter_bots_trad_social'
    DATASET = 'twitter_bots'
    POS_DESC = 'Tweets from traditional bots'
    NEG_DESC = 'Tweets from bots with social networks'
    POS = ['social_bot']
    NEG = ['trad_bot']
    ANNOTATIONS = ['talks about other people']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_twitter_misspellings_your_ur():
    """Tweets with and without an abbreviation of 'your' to 'ur'"""

    PAIR = 'twitter_misspellings_your_ur'
    DATASET = 'twitter_misspellings'
    POS_DESC = 'tweets that misspell your'
    NEG_DESC = 'tweets that don\'t misspell your'
    POS = ['your_misspell']
    NEG = ['your_proper']
    ANNOTATIONS = ['is part of a conversation','is more friendly']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_twitter_misspellings_with_wit():
    """Tweets with and without an abbreviation of 'with' to 'wit'"""

    PAIR = 'twitter_misspellings_with_wit'
    DATASET = 'twitter_misspellings'
    POS_DESC = 'tweets that misspell with'
    NEG_DESC = 'tweets that don\'t misspell with'
    POS = ['with_misspell']
    NEG = ['with_proper']
    ANNOTATIONS = ['is part of a conversation','is more friendly']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_twitter_misspellings_that_dat():
    """Tweets with and without an abbreviation of 'that' to 'dat'"""

    PAIR = 'twitter_misspellings_that_dat'
    DATASET = 'twitter_misspellings'
    POS_DESC = 'tweets that misspell that'
    NEG_DESC = 'tweets that don\'t misspell that'
    POS = ['that_misspell']
    NEG = ['that_proper']
    ANNOTATIONS = ['is part of a conversation','is more friendly']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_twitter_misspellings_going_goin():
    """Tweets with and without an abbreviation of 'going' to 'goin'"""

    PAIR = 'twitter_misspellings_going_goin'
    DATASET = 'twitter_misspellings'
    POS_DESC = 'tweets that misspell going'
    NEG_DESC = 'tweets that don\'t misspell going'
    POS = ['going_misspell']
    NEG = ['going_proper']
    ANNOTATIONS = ['is part of a conversation','is more friendly']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_unhealthy_conversations_dismissive_condescending():
    """Unhealthy conversations characterized as dismissive vs. condescending."""
    
    PAIR = 'unhealthy_conversations_dismissive_condescending'
    DATASET = 'unhealthy_conversations'
    POS_DESC = 'online messages that are dismissive'
    NEG_DESC = 'online messages that are condescending'
    POS = ['dismissive']
    NEG = ['condescending']
    ANNOTATIONS = ['is not insulting','is shorter']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_unhealthy_conversations_generalisation_unfair():
    """Unhealthy conversations characterized as generalisation (not unfair) vs. generalisation unfair."""

    PAIR = 'unhealthy_conversations_generalisation_unfair'
    DATASET = 'unhealthy_conversations'
    POS_DESC = 'online messages that generalize'
    NEG_DESC = 'online messages that generalize unfairly'
    POS = ['generalisation']
    NEG = ['generalisation_unfair']
    ANNOTATIONS = ['is more objective','provides more reasoning']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_unhealthy_conversations_hostile_antagonize():
    """Unhealthy conversations characterized as hostlie vs. antagonizing."""

    PAIR = 'unhealthy_conversations_hostile_antagonize'
    DATASET = 'unhealthy_conversations'
    POS_DESC = 'online messages that are hostile'
    NEG_DESC = 'online messages that are antagonizing'
    POS = ['hostile']
    NEG = ['antagonize']
    ANNOTATIONS = ['is less insulting','uses more curse words']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_yc_startups_exited_operating():
    """YC startups that either exited or are still operating."""

    PAIR = 'yc_startups_exited_operating'
    DATASET = 'yc_startups'
    POS_DESC = 'Y Combinator startup descriptions that have exited'
    NEG_DESC = 'Y Combinator startup descriptions that are still operating'
    POS = ['exited']
    NEG = ['operating']
    ANNOTATIONS = ['describes a tech company','talks about specific services']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_yc_startups_dead_operating():
    """YC startups that either dead or are still operating."""

    PAIR = 'yc_startups_dead_operating'
    DATASET = 'yc_startups'
    POS_DESC = 'Y Combinator startup descriptions that are dead'
    NEG_DESC = 'Y Combinator startup descriptions that are still operating'
    POS = ['dead']
    NEG = ['operating']
    ANNOTATIONS = ['describes less innovative companies']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_yc_startups_bay_area():
    """YC startups that either are or aren't in the Bay Area."""

    PAIR = 'yc_startups_bay_area'
    DATASET = 'yc_startups'
    POS_DESC = 'Y Combinator startup descriptions from the Bay Area'
    NEG_DESC = 'Y Combinator startup descriptions outisde the Bay Area'
    POS = ['bay_area']
    NEG = ['not_bay_area']
    ANNOTATIONS = ['describes a tech company','talks about machine learning']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

def pair_yc_startups_pre_post_2013():
    """YC startups between 2005-2012 and 2013-2014."""

    PAIR = 'yc_startups_pre_post_2013'
    DATASET = 'yc_startups'
    POS_DESC = 'Y Combinator startup descriptions from before 2013'
    NEG_DESC = 'Y Combinator startup descriptions from after 2013'
    POS = ['post_2013']
    NEG = ['pre_2013']
    ANNOTATIONS = ['describes a tech company','talks about machine learning']

    return generate_pair(PAIR, DATASET, POS_DESC, NEG_DESC, POS, NEG, ANNOTATIONS)

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
    pair_happy_moments_affection_bonding,
    pair_happy_moments_enjoying_leisure,
    pair_happy_moments_usa_india,
    pair_happy_moments_usa_venezuela,
    pair_happy_moments_usa_canada,
    pair_happy_moments_college_20s,
    pair_happy_moments_early_late_20s,
    pair_happy_moments_30s_40s,
    pair_happy_moments_gender,
    pair_happy_moments_parenthood,
    pair_happy_moments_marraige,
    pair_happy_moments_separation_divorce,
    pair_microedit_humor_unfunny_funny,
    pair_microedit_humor_funny_very_funny,
    pair_monster_jobs_atl_tampa,
    pair_monster_jobs_ca_tx,
    pair_monster_jobs_sf_nyc,
    pair_movie_popularity_hit_average,
    pair_movie_popularity_bad_average,
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
    pair_trial_deception_truth_lie,
    pair_tweet_gender_male_female,
    pair_tweet_rumor_redhawks_early_late,
    pair_tweet_rumor_zucc_early_late,
    pair_tweet_rumor_denzel_wash_early_late,
    pair_tweet_rumor_veggietales_early_late,
    pair_twitter_bots_human,
    pair_twitter_bots_trad_social,
    pair_twitter_misspellings_your_ur,
    pair_twitter_misspellings_with_wit,
    pair_twitter_misspellings_that_dat,
    pair_twitter_misspellings_going_goin,
    pair_unhealthy_conversations_dismissive_condescending,
    pair_unhealthy_conversations_generalisation_unfair,
    pair_unhealthy_conversations_hostile_antagonize,
    pair_yc_startups_exited_operating,
    pair_yc_startups_dead_operating,
    pair_yc_startups_bay_area,
    pair_yc_startups_pre_post_2013,
]

def main():

    # pbar = tqdm(enumerate(constructors[:13]))
    pairs = []

    for i, constructor in enumerate(constructors):
        # pbar.set_description(f'processing pair {i}')
        new_pair = constructor()
        describe_pair(new_pair)
        pairs.append(new_pair)

    
    json.dump(pairs, open(PAIRS_FILE, 'w'))

if __name__ == '__main__':
    main()