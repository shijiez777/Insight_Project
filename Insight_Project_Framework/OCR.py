# Script to run OCR on pdf files and output text into data/preprocessed.

import pytesseract
import numpy as np
from pdf2image import convert_from_path, convert_from_bytes
import os
from threading import Thread
import pickle
import queue
import multiprocessing
import sys
from helpers import *

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

# Function to convert single pdf to text and save
def doc2text(pdf_folder_path, text_folder_path, pdf_file_name, num_pages):
    '''
    Function to read single pdf document, parse the pdf into text using tesseract ocr, and store the text.

    Parameters:
    pdf_folder_path(string): the path to the folder storing PDF files
    text_folder_path(string): the path to the folder where the extracted text to be stored
    pdf_file_name(string): The name of the pdf file to be parsed.
    num_pages: number of pages of the pdf to extract texts.
    '''

    text_name = pdf_file_name.split('.')[0]
    images = convert_from_path(os.path.join(pdf_folder_path, pdf_file_name))
    tmp_texts = []
    # process the pages
    for i in range(len(images)):
        if i < num_pages:
            image = images[i]
            tmp_texts.append(pytesseract.image_to_string(image))

    # dump file using pickle
    text_file_name_full = os.path.join(text_folder_path, text_name) + '.pkl'        
    with open(text_file_name_full, 'wb') as filehandle:
        pickle.dump(tmp_texts, filehandle)
    
    del images
    del tmp_texts
    return

def bytes2text(request_content, num_pages):
    images = convert_from_bytes(request_content)

    tmp_texts = []
    for i in range(len(images)):
        if i < num_pages:
            image = images[i]
            tmp_texts.append(pytesseract.image_to_string(image))
    return tmp_texts

# threadmanager class for running multithreading.
class ThreadManger(Thread):

    def __init__(self, queue):
        super(ThreadManger, self).__init__()
        self.queue = queue

    def run(self):
        while self.queue.qsize() > 0:
            # Run the tasks as long as there are files to be processed.
            items = self.queue.get()
            method = items[0]
            args = items[1:]
            method(*args)
            print("# tasks left: " + str(self.queue.qsize()), end = '\r')
            del method 
            del args
            self.queue.task_done()
        print("\n Thread job complete.")

    # def run(self):
    #     while True:
    #         # Run the tasks as long as there are files to be processed.
    #         if self.queue.qsize() > 0:
    #             items = self.queue.get()
    #             method = items[0]
    #             args = items[1:]
    #             method(*args)
    #             print("# tasks left: " + str(self.queue.qsize()), end = '\r')
    #             del method 
    #             del args
    #             self.queue.task_done()


def threaded_OCR(pdf_folder_path, text_folder_path, config):
    # check if directory exists. If not, create
    ensure_dir(text_folder_path)

    pdf_files = os.listdir(pdf_folder_path)
    text_files = os.listdir(text_folder_path)

    # find all PDF ids in the pdf folder
    pdf_ids = []
    for i in range(len(pdf_files)):
        pdf_ids.append(pdf_files[i].split('.')[0])
    pdf_ids = np.array(pdf_ids)

    # find all text ids in the text folder
    for j in range(len(text_files)):
        text_files[j] = text_files[j].split('.')[0]

    # find files that are NOT YET PROCESSED
    unprocessed_pdf_ids = np.setdiff1d(pdf_ids, text_files)
    unprocessed_pdf_files = []
    for k in range(len(unprocessed_pdf_ids)):
        idx = np.where(unprocessed_pdf_ids[k] == pdf_ids)[0][0]
        if pdf_files[idx][-3:] == 'pdf':
            unprocessed_pdf_files.append(pdf_files[idx])

    print("# Files to be OCRed: " + str(len(unprocessed_pdf_files)))

    # add task to queue
    Q = queue.Queue(len(unprocessed_pdf_files))
    for i in range(len(unprocessed_pdf_files)):
        Q.put((doc2text, pdf_folder_path, text_folder_path, unprocessed_pdf_files[i], config["num_pages"]))

    # start the multithread processing.
    for l in range(config["num_cores"]):
        print("starting thread no %s" % l)
        thread = ThreadManger(Q)
        thread.start()
    thread.join()

# MULTITHREAD PROCESS
if __name__ == "__main__":
    config_path = "../configs/config.yml"
    config = read_yaml(config_path)

    # move to data directory
    os.chdir(config['data_path'])
    pdf_folder_path = 'raw/complaints'
    text_folder_path = 'preprocessed/complaints'

    threaded_OCR(pdf_folder_path, text_folder_path, config)

    # ensure_dir(pdf_folder_path)
    # ensure_dir(text_folder_path)

    # pdf_files = os.listdir(pdf_folder_path)
    # text_files = os.listdir(text_folder_path)

    # find all PDF ids in the pdf folder
    # pdf_ids = []
    # for i in range(len(pdf_files)):
    #     pdf_ids.append(pdf_files[i].split('.')[0])
    # pdf_ids = np.array(pdf_ids)

    # find all text ids in the text folder
    # for j in range(len(text_files)):
    #     text_files[j] = text_files[j].split('.')[0]

    # find files that are NOT YET PROCESSED
    # unprocessed_pdf_ids = np.setdiff1d(pdf_ids, text_files)
    # unprocessed_pdf_files = []
    # for k in range(len(unprocessed_pdf_ids)):
    #     idx = np.where(unprocessed_pdf_ids[k] == pdf_ids)[0][0]
    #     if pdf_files[idx][-3:] == 'pdf':
    #         unprocessed_pdf_files.append(pdf_files[idx])

    # print("# Files to be OCRed: " + str(len(unprocessed_pdf_files)))

    # add task to queue
    # Q = queue.Queue(len(unprocessed_pdf_files))
    # for i in range(len(unprocessed_pdf_files)):
    #     Q.put((doc2text, pdf_folder_path, text_folder_path, unprocessed_pdf_files[i], config["num_pages"]))

    # start the multithread processing.
    # for l in range(config["num_cores"]):
    #     print("starting thread no %s" % l)
    #     thread = ThreadManger(Q)
    #     thread.start()
    #     thread.join()