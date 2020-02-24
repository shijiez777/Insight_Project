import os
from pdf2image import convert_from_path
from helpers import *
import pytesseract


config_path = "../configs/config.yml"
config = read_yaml(config_path)

model_path = os.path.join(config["model_folder"], config["model_name"])

c = load_model(model_path)

pdf_folder_path = config["prediction_pdf_path"]
file_name = "1.pdf"

images = convert_from_path(os.path.join(pdf_folder_path, file_name))
num_pages = config["num_pages"]
images = images[:num_pages]


texts = []
for i in range(len(images)):
    texts.append(pytesseract.image_to_string(images[i]))

cleaned_text = c.word_processor.clean_and_concatenate_text(texts)
X_pred = c.feature_vectorizer.transform([cleaned_text])
y_pred = c.clf.predict(X_pred)
result_le_inverse = c.le.inverse_transform(y_pred)
print(config["key_county_mapping"][result_le_inverse[0]])
