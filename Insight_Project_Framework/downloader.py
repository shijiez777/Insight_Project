# Download data from metadata csv in data/metadata to data/raw

import pandas as pd
import os
import requests
import json
from io import BytesIO
import pycurl
import queue

# function for downloading complaint and judgement documents from metadata csv.
def download_files(folder_name, df, start_index = 0):
    '''
    Function that downloads all the pdf files from the dataset.
    
    Reads in from the csv, send query to the API and retrieve PDF and save to the local directory.

    Parameters:
    folder_name(string): path to store the pdf files.
    df(np.DataFrame): dataframe containing the metadata of pdfs.
    start_index(int): index of files in dataframe to begin download, optional.
    '''

    print("Downloading " + folder_name + " docs...")
    if folder_name not in os.listdir():
        os.mkdir(folder_name)
    for i in range(start_index, len(df)):
        url = df['poc_file_path'][i]
        file_name = df['document_id'][i] + '.' + url.split('.')[-1]
        # retrieve doc from URL.
        myfile = requests.get(url, allow_redirects=True)
        open(os.path.join(folder_name, file_name), 'wb').write(myfile.content)
        print(i, end='\r')
    print("Done")

if __name__ == "__main__":
    os.chdir(os.environ['data_dir'])
    raw_data_folder = 'raw'
    metadata_folder = os.path.join(raw_data_folder, 'metadata')
    # change to metadata folder and read metadata csv
    os.chdir(metadata_folder)
    complaints = pd.read_csv('complaint_meta.csv')
    # change to folder for storing the data
    complaint_folder = 'complaints'
    os.chdir("..")
    # serial downloading
    start_index = len(os.listdir(complaint_folder))
    print("start index: " + str(start_index))
    download_files(complaint_folder, complaints, start_index)