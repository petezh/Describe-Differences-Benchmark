import requests
import zipfile
from io import BytesIO
import tarfile
from os.path import join
import shutil
import json
from typing import Dict
import os
import gdown

from parameters import *

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