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

rawDataFolder = '../data/raw'
metadataFolder = os.path.join(rawDataFolder, 'metadata')

# complaintFolder = os.path.join(rawDataFolder, 'complaints')
# judgementFolder = os.path.join(rawDataFolder, 'judgements')
# countyComplaintFolder = os.path.join(rawDataFolder, 'countyComplaints')

complaintFolder = 'complaints'
judgementFolder = 'judgements'
countyComplaintFolder = 'countyComplaints'

os.chdir(metadataFolder)

complaints = pd.read_csv('complaint_meta.csv')
judgements = pd.read_csv('judgement_meta.csv')
poc_complaint = pd.read_csv('poc_complaint.csv')

os.chdir("..")
# function for downloading complaint and judgement documents from metadata csv.
def downloadFiles(folderName, df, startIdx = 0):
    print("Downloading " + folderName + " docs...")
    if folderName not in os.listdir():
        os.mkdir(folderName)

    for idx in range(startIdx, len(df)):
        url = df['poc_file_path'][idx]
        fileName = url.split('/')[-1]
        myfile = requests.get(url, allow_redirects=True)
        open(os.path.join(folderName, fileName), 'wb').write(myfile.content)

        print(idx, end='\r')
    print("Done")

# function for downloading poc_complaint.
def downloadPOCComplaintFiles(folderName, df, startIdx = 0):
    print("Downloading " + folderName + " docs...")

    if folderName not in os.listdir():
        os.mkdir(folderName)

    c = pycurl.Curl()
    c.setopt(pycurl.HTTPHEADER, ["x-api-key: rYRv7klUYJa9bFj0MbM3F6YCPE8kTCWH4DxiycxQ"])

    for idx in range(startIdx, len(df)): 
        document_id = df['document_id'][idx]
        url = "https://doc-poc.unicourt.com/v1/getdocument?document_id=" + document_id

        c.setopt(c.URL, url)
        buffer = BytesIO()

        c.setopt(c.WRITEDATA, buffer)
        c.perform()

        tmp = buffer.getvalue().decode('utf-8')
        pdfUrl = json.loads(tmp)['url']
    
        fileName = pdfUrl.split('/')[5].split('?')[0]
        myfile = requests.get(pdfUrl, allow_redirects=True)
        open(os.path.join(folderName, fileName), 'wb').write(myfile.content)

        print(idx, end='\r')
    c.close()
    print("Done")

downloadFiles(complaintFolder, complaints)
downloadFiles(judgementFolder, judgements)
downloadPOCComplaintFiles(countyComplaintFolder, poc_complaint)