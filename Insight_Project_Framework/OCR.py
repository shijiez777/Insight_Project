# Script to run OCR on pdf files and output text into data/preprocessed.

import pytesseract
import numpy as np
from pdf2image import convert_from_path
import os

import pickle

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)







# import cv2

# denoising function
# def denoise(img):
#     # kernel = np.ones((kernelSize, kernelSize), np.uint8)
#     denoised = img
#     # grayscale performs better than Binary as it provides more information
#     return denoised
# 

# read documents from a folder in raw data, OCR and save result in folder in preprocessed
def pdf2text(pdf_folder_path, text_folder_path, start_index=0):
    print("converting pdf in " + pdf_folder_path + " to text and saving in " + text_folder_path)

    if text_folder_path.split('/')[1] not in os.listdir('preprocessed'):
        os.mkdir(text_folder_path)

    files = os.listdir(pdf_folder_path)
    print("total file #:", str(len(files)))
    for i in range(start_index, len(files)):
        pdf_file = files[i]

        text_name = pdf_file.split('.')[0]
        images = convert_from_path(os.path.join(pdf_folder_path, pdf_file))
        tmp_texts = []
        for image in images:
            tmp_texts.append(pytesseract.image_to_string(image))
        # dump file using pickle
        text_file_name = os.path.join(text_folder_path, text_name) + '.pkl'
        
        # 
        print("text file: " + text_name)
        #
        
        with open(text_file_name, 'wb') as filehandle:
            pickle.dump(tmp_texts, filehandle)
        print(i, end='\r')
        # break for testing
        if i == 10:
            break
    print("Done")


def read_pickle(text_folder_path, id):
    file_names = os.listdir(text_folder_path)
    with open(os.path.join(text_folder_path, file_names[id]), 'rb') as filehandle:
        # read the data as binary data stream
        read_text = pickle.load(filehandle)
    return read_text



# #move to data directory
os.chdir(os.environ['Insight_Project'])

os.chdir('data')

# # Process complaints
# pdf_folder_path = 'raw/complaints'
# text_folder_path = 'preprocessed/complaints'
# pdf2text(pdf_folder_path, text_folder_path)

# process judgements
pdf_folder_path = 'raw/judgements'
text_folder_path = 'preprocessed/judgements'
pdf2text(pdf_folder_path, text_folder_path)

# Process countyComplaints
pdf_folder_path = 'raw/countyComplaints'
text_folder_path = 'preprocessed/countyComplaints'
pdf2text(pdf_folder_path, text_folder_path)