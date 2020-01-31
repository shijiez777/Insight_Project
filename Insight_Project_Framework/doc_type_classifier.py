import pickle
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn import preprocessing
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score


def read_pickle(text_folder_path, file_name):

    with open(os.path.join(text_folder_path, file_name), 'rb') as filehandle:
        # read the data as binary data stream
        read_text = pickle.load(filehandle)
    return read_text


def clean_text(text):
    regex = re.compile(r'[\n\r\t]')
    cleaned = regex.sub("", text)
    return cleaned

def load_data_and_clean(text_folder_path):
    corpus = []
    labels = []

    files = os.listdir(text_folder_path)
    for file_name in files:
        text = read_pickle(text_folder_path, file_name)
        cleaned_text = clean_text(text)
        corpus.append(cleaned_text)
        labels.append(file_name.split('_')[1])

    return corpus, labels

# def load_label(text_folder_path):
#     files = os.listdir(text_folder_path)
#     labels = []
#     for file_name in files:
#         labels.append(file_name.split('_')[1])
#     return labels

def compute_TFIDF(corpus):
    vectorizer = TfidfVectorizer()
    vec = vectorizer.fit_transform(corpus)
    return vec

# simple predict
def simple_inference(keys, corpus, encoded_labels, county_names):
    correct_preds = 0
    result_DF = pd.DataFrame(np.zeros((len(corpus), len(keys))), columns = county_names)
    for i in range(len(corpus)):
        doc = corpus[i]
        for j in range(len(county_names)):
            county_name = county_names[j]
            if county_name in doc.lower():
                result_DF.loc[i, county_name] = 1
    
    for i in range(len(result_DF)):
        if np.sum(result_DF.loc[i]) == 1 and np.where(result_DF.loc[i] == 1)[0][0] == encoded_labels[i]:
            correct_preds += 1
    print("baseline accuracy: " + str(correct_preds/len(encoded_labels)))

def train(X_train, y_train):
    clf = svm.LinearSVC()
    clf.fit(X_train, y_train)
    return clf


if __name__ == "__main__":
    os.chdir(os.environ['data_dir'])
    text_folder = 'preprocessed/complaints'
    keys = ['FRE', 'KC', 'LA', 'SCL', 'SFC', 'SM']
    county_names = ['fresno', 'kern', 'los angeles', 'santa clara', 'san francisco', 'san mateo']
    corpus, labels = load_data_and_clean(text_folder)

    print("# documents: " + str(len(corpus)))

    le = preprocessing.LabelEncoder()
    le.fit(labels)
    encoded_labels = le.transform(labels)
    tf_idf_vector = compute_TFIDF(corpus)

    simple_inference(keys, corpus, encoded_labels, county_names)

    clf = svm.LinearSVC()
    print(cross_val_score(clf, tf_idf_vector, encoded_labels, cv=5, scoring='accuracy'))

    # test_file_idx = 0
    # files = os.listdir(text_folder)
    # print("file name: " + files[test_file_idx])
    # print(le.inverse_transform(clf.predict(tf_idf_vector[test_file_idx, :])))


    # label_key_dict = {}
    # >>> le.classes_
    # array(['FRE', 'KC', 'LA', 'SCL', 'SFC', 'SM'], dtype='<U3')

    # for i in range(len(keys)):
    #     label_key_dict[keys[i]] = county_names[i]






# test
# read_pickle('../data/preprocessed/complaints', 'CA_FRE_01edFpSp4-OjCoEZwI46FA2.pkl')