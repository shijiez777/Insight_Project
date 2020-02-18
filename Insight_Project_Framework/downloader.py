"""Download data from metadata csv in data/metadata to data/raw."""

import pandas as pd
import requests
import json
from io import BytesIO
import pycurl
import queue
from helpers import *


# function for downloading complaint and judgement documents from metadata csv.
def download_files(folder_name, df, start_index = 0):
    """
    Download all the pdf files from the dataset.
    
    Reads in from the csv, send query to the API and retrieve PDF and save to the local directory.

    Parameters:
    folder_name(string): path to store the pdf files.
    df(np.DataFrame): dataframe containing the metadata of pdfs.
    start_index(int): index of files in dataframe to begin download, optional.
    """
    print("Downloading " + folder_name + " docs...")
    # os.chdir(folder_name)
    # if folder_name not in os.listdir():
    #     os.mkdir(folder_name)
    for i in range(start_index, len(df)):
        url = df['poc_file_path'][i]
        file_name = df['document_id'][i] + '.' + url.split('.')[-1]
        # retrieve doc from URL.
        myfile = requests.get(url, allow_redirects=True)
        # open(os.path.join(folder_name, file_name), 'wb').write(myfile.content)
        with open(file_name, 'wb') as file_handle:
            file_handle.write(myfile.content)

        print(i, end='\r')
    print("\nDone")


def download_file_by_id(document_id):
    c = pycurl.Curl()
    c.setopt(pycurl.HTTPHEADER, ["x-api-key: rYRv7klUYJa9bFj0MbM3F6YCPE8kTCWH4DxiycxQ"])
    url = "https://doc-poc.unicourt.com/v1/getdocument?document_id=" + document_id
    c.setopt(c.URL, url)
    buffer = BytesIO()
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    tmp = buffer.getvalue().decode('utf-8')
    pdf_url = json.loads(tmp)['url']
    myfile = requests.get(pdf_url, allow_redirects=True)
    c.close()
    return myfile.content

if __name__ == "__main__":

    config_path = "../configs/config.yml"
    config = read_yaml(config_path)

    # os.chdir(config['data_path'])
    # metadata_folder = os.path.join(config['data_path'], 'raw/metadata')# 'raw/metadata'
    
    # change to metadata folder and read metadata csv
    # os.chdir(config["metadata_folder"])
    complaints = pd.read_csv(os.path.join(config["metadata_folder"], 'complaint_meta.csv'))
    # change to folder for storing the data
    
    
    training_pdf_folder = config["training_pdf_folder"]
    # complaint_folder = '../complaints'
    ensure_dir(training_pdf_folder)
    # os.chdir(training_pdf_folder)
    # serial downloading
    start_index = len(os.listdir(training_pdf_folder))
    print("start index: " + str(start_index))
    download_files(training_pdf_folder, complaints, start_index)




    # os.chdir(config['data_path'])
    # raw_data_folder = 'raw'
    # metadata_folder = os.path.join(raw_data_folder, 'metadata')
    # # change to metadata folder and read metadata csv
    # os.chdir(metadata_folder)
    # complaints = pd.read_csv('complaint_meta.csv')
    # # change to folder for storing the data
    # complaint_folder = 'complaints'
    # os.chdir("..")
    # # serial downloading
    # start_index = len(os.listdir(complaint_folder))
    # print("start index: " + str(start_index))
    # download_files(complaint_folder, complaints, start_index)