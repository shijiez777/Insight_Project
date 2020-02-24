import os
import streamlit as st
from pdf2image import convert_from_path
from helpers import *
import pytesseract

config_path = "../configs/config.yml"
config = read_yaml(config_path)
model_path = os.path.join(config["model_folder"], config["model_name"])
c = load_model(model_path)

pdf_folder_path = config["prediction_pdf_path"]
num_pages = config["num_pages"]
key_county_mapping = config["key_county_mapping"]

st.title("LeDoC county classification")
classification_placeholder = st.empty()

def file_selector(folder_path):
    filenames = os.listdir(folder_path)
    filenames.sort()
    filenames = ["-"] + filenames
    selected_filename = st.sidebar.selectbox('Select a file', filenames)
    return os.path.join(selected_filename)

file_name = file_selector(pdf_folder_path)
if file_name == "-":
    st.warning('Please select a file.')
    raise st.ScriptRunner.StopException

# load pdf and display first image
images = convert_from_path(os.path.join(pdf_folder_path, file_name))
images = images[:num_pages]
st.image(images[0], width=5, use_column_width=True)

# OCR the text and predict
texts = []
for i in range(len(images)):
    texts.append(pytesseract.image_to_string(images[i]))
cleaned_text = c.word_processor.clean_and_concatenate_text(texts)
X_pred = c.feature_vectorizer.transform([cleaned_text])
y_pred = c.clf.predict(X_pred)
result_le_inverse = c.le.inverse_transform(y_pred)
cls_text = st.header("classification: ")
classification_placeholder.header('Classification: ' + key_county_mapping[result_le_inverse[0]])
