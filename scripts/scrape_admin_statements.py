from utils import *
from parameters import *

import glob
import pdfplumber

def scrape():

    NAME = 'admin_statements'

    directory = f'{DOWNLOAD_FOLDER}/{NAME}'
    
    administrations = ['44-Obama', '45-Trump', '46-Biden']

    data = {}

    for admin in administrations:
        print(admin)

        files = glob.glob(f'{directory}/statements-of-administration-policy-main/archive/statements/{admin}/**/*.pdf')

        statements = []

        for file in files:
            text = ""
            try:
                with pdfplumber.open(file) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + " "
                statements.append(text)
            except:
                pass

        data[admin] = statements
    
    return data