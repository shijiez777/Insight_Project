# Download data from metadata csv in data/metadata to data/raw

import pandas as pd
import os
import requests
import json
from io import BytesIO
import pycurl


# try:
#     from PIL import Image
# except ImportError:
#     import Image
# import pytesseract

raw_data_folder = '../data/raw'
metadata_folder = os.path.join(raw_data_folder, 'metadata')

# complaint_folder = os.path.join(raw_data_folder, 'complaints')
# judgementFolder = os.path.join(raw_data_folder, 'judgements')
# county_complaint_folder = os.path.join(raw_data_folder, 'countyComplaints')

complaint_folder = 'complaints'
judgementFolder = 'judgements'
county_complaint_folder = 'countyComplaints'

os.chdir(metadata_folder)

complaints = pd.read_csv('complaint_meta.csv')
judgements = pd.read_csv('judgement_meta.csv')
poc_complaint = pd.read_csv('poc_complaint.csv')

os.chdir("..")
# function for downloading complaint and judgement documents from metadata csv.
def download_files(folder_name, df, start_idx = 0):
    print("Downloading " + folder_name + " docs...")
    if folder_name not in os.listdir():
        os.mkdir(folder_name)

    for i in range(start_idx, len(df)):
        url = df['poc_file_path'][i]
        file_name = url.split('/')[-1]
        myfile = requests.get(url, allow_redirects=True)
        open(os.path.join(folder_name, file_name), 'wb').write(myfile.content)

        print(i, end='\r')
    print("Done")

# function for downloading poc_complaint.
def download_POC_complaint_files(folder_name, df, start_idx = 0):
    print("Downloading " + folder_name + " docs...")

    if folder_name not in os.listdir():
        os.mkdir(folder_name)

    c = pycurl.Curl()
    c.setopt(pycurl.HTTPHEADER, ["x-api-key: rYRv7klUYJa9bFj0MbM3F6YCPE8kTCWH4DxiycxQ"])

    for i in range(start_idx, len(df)): 
        document_id = df['document_id'][i]
        url = "https://doc-poc.unicourt.com/v1/getdocument?document_id=" + document_id

        c.setopt(c.URL, url)
        buffer = BytesIO()

        c.setopt(c.WRITEDATA, buffer)
        c.perform()

        tmp = buffer.getvalue().decode('utf-8')
        pdf_url = json.loads(tmp)['url']
    
        file_name = pdf_url.split('/')[5].split('?')[0]
        myfile = requests.get(pdf_url, allow_redirects=True)
        open(os.path.join(folder_name, file_name), 'wb').write(myfile.content)

        print(i, end='\r')
    c.close()
    print("Done")

download_files(complaint_folder, complaints)
download_files(judgementFolder, judgements)
download_POC_complaint_files(county_complaint_folder, poc_complaint)