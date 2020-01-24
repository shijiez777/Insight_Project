# Script to run OCR on pdf files and output text into data/preprocessed.

import pytesseract
import numpy as np
from pdf2image import convert_from_path
import os

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
        
        #
        print(pdf_file)
        #
        
        text_name = pdf_file.split('.')[0]
        images = convert_from_path(os.path.join(pdf_folder_path, pdf_file))
        tmp_texts = []
        for image in images:
            tmp_texts.append(pytesseract.image_to_string(image))
        # dump file using pickle
        txt_file_name = os.path.join(text_folder_path, text_name) + '.pkl'
        with open(txt_file_name, 'wb') as filehandle:
            pickle.dump(tmp_texts, filehandle)
        print(i, end='\r')
        # break for testing
        if i == 10:
            break
    print("Done")

#move to data directory
os.chdir(os.environ['Insight_Project'])

os.chdir('data')

pdf_folder_path = 'raw/complaints'
text_folder_path = 'preprocessed/complaints'
pdf2text(pdf_folder_path, text_folder_path)
