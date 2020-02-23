import numpy as np
import os
from matplotlib import pyplot as plt
# import plotly.graph_objects as go
import streamlit as st

#Custom python files
# from model.model import *
# from training import *
# from util.dataloader import *
# from util.data_process import *

import os
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

def file_selector(folder_path):
    filenames = os.listdir(folder_path)
    selected_filename = st.sidebar.selectbox('Select a file', filenames)
    return os.path.join(selected_filename)

file_name = file_selector(pdf_folder_path)

images = convert_from_path(os.path.join(pdf_folder_path, file_name))
images = images[:num_pages]


st.image(images[0], caption='Sunrise by the mountains', use_column_width=True)


texts = []
for i in range(len(images)):
    texts.append(pytesseract.image_to_string(images[i]))

cleaned_text = c.word_processor.clean_and_concatenate_text(texts)
X_pred = c.feature_vectorizer.transform([cleaned_text])
y_pred = c.clf.predict(X_pred)
result_le_inverse = c.le.inverse_transform(y_pred)
print(key_county_mapping[result_le_inverse[0]])





# sample_graph = model_used.get_prediction_from_file(inputs)
# prob = sample_graph.numpy().squeeze()

# time_stamp = 0.5*np.arange(len(prob))

# fig = go.Figure()
# fig.add_trace(go.Scatter(x=time_stamp, y=prob, mode='lines',
#                         hovertemplate='Time: %{x} min<br>Radiant Win Probability: %{y:.2f}', name='', showlegend = False))
# fig.add_shape(
#         # Line Horizontal
#         go.layout.Shape(
#             type="line",
#             x0=0,
#             y0=0.5,
#             x1=time_stamp[-1],
#             y1=0.5,
#             line=dict(
#                 color="Black",
#                 width=1,
#             ),
#     ))

# fig['layout']['yaxis1'].update(title='',range=[0, 1], autorange=False)

# st.plotly_chart(fig)
