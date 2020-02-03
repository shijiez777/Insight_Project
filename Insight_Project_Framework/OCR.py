# Script to run OCR on pdf files and output text into data/preprocessed.

import pytesseract
import numpy as np
from pdf2image import convert_from_path
import os
from threading import Thread

import pickle

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

import queue
import multiprocessing


import sys
# sys.path.insert(1, 'Tolstoy-UniCourt')
# from main import pdf_to_txt


# read documents from a folder in raw data, OCR and save result in folder in preprocessed
def doc2text(pdf_folder_path, text_folder_path, start_index=0):
    doc_dict = {}
    print("converting pdf in " + pdf_folder_path + " to text and saving in " + text_folder_path)

    if text_folder_path.split('/')[1] not in os.listdir('preprocessed'):
        os.mkdir(text_folder_path)

    files = os.listdir(pdf_folder_path)
    print("total file #:", str(len(files)))
    for i in range(start_index, len(files)):
        pdf_file = files[i]
        if pdf_file.split('.')[-1] == 'pdf':
            text_name = pdf_file.split('.')[0]
            # tmp_text = pdf_to_txt(os.path.join(pdf_folder_path, pdf_file))
            
            images = convert_from_path(os.path.join(pdf_folder_path, pdf_file))
            tmp_texts = []
            for image in images:
                tmp_texts.append(pytesseract.image_to_string(image))
            # dump file using pickle
            
            text_file_name = os.path.join(text_folder_path, text_name) + '.pkl'        
            with open(text_file_name, 'wb') as filehandle:
                pickle.dump(tmp_texts, filehandle)
            print(i, end='\r')

            # doc_dict[text_name] = tmp_texts
    #         text_file_name = os.path.join(text_folder_path, 'extracted_text') + '.pkl'
    #         print(i, end='\r')
    #         if i % 100 == 0:
    #             with open(text_file_name, 'wb') as filehandle:
    #                 pickle.dump(doc_dict, filehandle)
    # with open(text_file_name, 'wb') as filehandle:
    #     pickle.dump(doc_dict, filehandle)
            
        # break for testing
        # if i == 1000:
        #     break
    print("Done")


# read documents from a folder in raw data, OCR and save result in folder in preprocessed
# def doc2text(pdf_folder_path, text_folder_path, start_index=0):
#     print("converting pdf in " + pdf_folder_path + " to text and saving in " + text_folder_path)

#     if text_folder_path.split('/')[1] not in os.listdir('preprocessed'):
#         os.mkdir(text_folder_path)

#     files = os.listdir(pdf_folder_path)
#     print("total file #:", str(len(files)))
#     for i in range(start_index, len(files)):
#         pdf_file = files[i]
#         if pdf_file.split('.')[-1] == 'pdf':
#             text_name = pdf_file.split('.')[0]
#             tmp_text = pdf_to_txt(os.path.join(pdf_folder_path, pdf_file))
#             # # dump file using pickle
#             text_file_name = os.path.join(text_folder_path, text_name) + '.pkl'        
#             with open(text_file_name, 'wb') as filehandle:
#                 pickle.dump(tmp_text, filehandle)
#             print(i, end='\r')
#         # break for testing
#         # if i == 1000:
#         #     break
#     print("Done")


def read_pickle(text_folder_path, id):
    file_names = os.listdir(text_folder_path)
    with open(os.path.join(text_folder_path, file_names[id]), 'rb') as filehandle:
        # read the data as binary data stream
        read_text = pickle.load(filehandle)
    return read_text


# Function to convert single pdf to text and save
def doc2text_single(pdf_folder_path, text_folder_path, pdf_file_name):
    text_name = pdf_file_name.split('.')[0]

    images = convert_from_path(os.path.join(pdf_folder_path, pdf_file_name))
    tmp_texts = []
    # for image in images:
    #     tmp_texts.append(pytesseract.image_to_string(image))

    print(pdf_file_name)
    
    for i in range(len(images)):
        if i <= 1:
            # print(i)
            image = images[i]
            tmp_texts.append(pytesseract.image_to_string(image))

    # dump file using pickle
    text_file_name_full = os.path.join(text_folder_path, text_name) + '.pkl'        
    with open(text_file_name_full, 'wb') as filehandle:
        pickle.dump(tmp_texts, filehandle)
    
    del images
    del tmp_texts

    print("Done")

# threadmanager class for running multithreading.
class ThreadManger(Thread):

    def __init__(self, queue):
        super(ThreadManger, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            if self.queue.qsize() > 0:
                items = self.queue.get()
                method = items[0]
                args = items[1:]
                method(*args)
                print("# tasks left: " + str(self.queue.qsize()))
                self.queue.task_done()

# SINGLE THREAD PROCESS
# if __name__ == "__main__":
#     # #move to data directory
#     # os.chdir(os.environ['Insight_Project'])

#     # os.chdir('data')
#     # data_folder = '/home/shijiez/googleBucket/data'
#     # os.chdir(data_folder)
#     os.chdir(os.environ['data_dir'])


#     # # Process complaints
#     pdf_folder_path = 'raw/complaints'
#     text_folder_path = 'preprocessed/complaints'

#     start_index = len(os.listdir(text_folder_path))
#     print("start index: " + str(start_index))

#     doc2text(pdf_folder_path, text_folder_path, start_index)


# MULTITHREAD PROCESS
if __name__ == "__main__":
    # #move to data directory
    os.chdir(os.environ['data_dir'])

    pdf_folder_path = 'raw/complaints'
    text_folder_path = 'preprocessed/complaints'

    pdf_files = os.listdir(pdf_folder_path)
    text_files = os.listdir(text_folder_path)

    pdf_ids = []
    for i in range(len(pdf_files)):
        pdf_ids.append(pdf_files[i].split('.')[0])
    pdf_ids = np.array(pdf_ids)

    for j in range(len(text_files)):
        text_files[j] = text_files[j].split('.')[0]

    # find files that are NOT YET PROCESSED
    unprocessed_pdf_ids = np.setdiff1d(pdf_ids, text_files)

    unprocessed_pdf_files = []
    for k in range(len(unprocessed_pdf_ids)):
        idx = np.where(unprocessed_pdf_ids[k] == pdf_ids)[0][0]
        # print(idx)
        if pdf_files[idx][-3:] == 'pdf':
            unprocessed_pdf_files.append(pdf_files[idx])

    print("# Files to be OCRed: " + str(len(unprocessed_pdf_files)))

    # add task to queue
    Q = queue.Queue(len(unprocessed_pdf_files))
    for i in range(len(unprocessed_pdf_files)):
        Q.put((doc2text_single, pdf_folder_path, text_folder_path, unprocessed_pdf_files[i]))

    num_cores = int(multiprocessing.cpu_count()/4)

    for l in range(num_cores):
        print("starting thread no %s" % l)
        thread = ThreadManger(Q)
        thread.start()

