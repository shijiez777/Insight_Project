# Script to run OCR on pdf files and output text into data/preprocessed.

# import pytesseract
import numpy as np
# from pdf2image import convert_from_path
import os

import pickle



# from pdf2image.exceptions import (
#     PDFInfoNotInstalledError,
#     PDFPageCountError,
#     PDFSyntaxError
# )


import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, 'Tolstoy-UniCourt')


# os.chdir('Tolstoy-UniCourt')
# print(os.getcwd())
# print(os.listdir())

from main_func import pdf_to_txt
# import main_func





# import cv2

# denoising function
# def denoise(img):
#     # kernel = np.ones((kernelSize, kernelSize), np.uint8)
#     denoised = img
#     # grayscale performs better than Binary as it provides more information
#     return denoised
# 

# read documents from a folder in raw data, OCR and save result in folder in preprocessed
def doc2text(pdf_folder_path, text_folder_path, start_index=0):
    print("converting pdf in " + pdf_folder_path + " to text and saving in " + text_folder_path)

    if text_folder_path.split('/')[1] not in os.listdir('preprocessed'):
        os.mkdir(text_folder_path)

    files = os.listdir(pdf_folder_path)
    print("total file #:", str(len(files)))
    for i in range(start_index, len(files)):
        pdf_file = files[i]
        if pdf_file.split('.')[-1] == 'pdf':
            text_name = pdf_file.split('.')[0]
            tmp_text = pdf_to_txt(os.path.join(pdf_folder_path, pdf_file))
            
            # images = convert_from_path(os.path.join(pdf_folder_path, pdf_file))
            # tmp_texts = []
            # for image in images:
            #     tmp_texts.append(pytesseract.image_to_string(image))
            # # dump file using pickle
            text_file_name = os.path.join(text_folder_path, text_name) + '.pkl'        
            with open(text_file_name, 'wb') as filehandle:
                pickle.dump(tmp_text, filehandle)
            print(i, end='\r')
        # break for testing
        if i == 1000:
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
pdf_folder_path = 'raw/complaints'
text_folder_path = 'preprocessed/complaints'
doc2text(pdf_folder_path, text_folder_path)

# process judgements
# pdf_folder_path = 'raw/judgements'
# text_folder_path = 'preprocessed/judgements'
# pdf2text(pdf_folder_path, text_folder_path)

# Process countyComplaints
# pdf_folder_path = 'raw/countyComplaints'
# text_folder_path = 'preprocessed/countyComplaints'
# pdf2text(pdf_folder_path, text_folder_path)