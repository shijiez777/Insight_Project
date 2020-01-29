import pickle
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn import preprocessing

def read_pickle(text_folder_path, file_name):

    with open(os.path.join(text_folder_path, file_name), 'rb') as filehandle:
        # read the data as binary data stream
        read_text = pickle.load(filehandle)
    return read_text


def clean_text(text):
    regex = re.compile(r'[\n\r\t]')
    cleaned = regex.sub("", text)
    return cleaned

def load_text_and_clean(text_folder_path):
    corpus = []
    files = os.listdir(text_folder_path)
    for file_name in files:
        text = read_pickle(text_folder_path, file_name)
        cleaned_text = clean_text(text)
        corpus.append(cleaned_text)
    return corpus

def load_label(text_folder_path):
    files = os.listdir(text_folder_path)
    labels = []
    for file_name in files:
        labels.append(file_name.split('_')[1])
    le = preprocessing.LabelEncoder()
    le.fit(labels)
    labels = le.transform(labels)
    return labels, le

def compute_TFIDF(corpus):
    vectorizer = TfidfVectorizer()
    vec = vectorizer.fit_transform(corpus)
    return vec

def train(text_folder_path):
    corpus = load_text_and_clean(text_folder_path)
    labels,le = load_label(text_folder_path)
    tf_idf_vector = compute_TFIDF(corpus)
    clf = svm.LinearSVC()
    clf.fit(tf_idf_vector, labels)
    return clf, le, tf_idf_vector

text_folder = os.path.join('../data/preprocessed/complaints')
clf, le, tf_idf_vector = train(text_folder)

test_file_idx = 0
files = os.listdir(text_folder)
print("file name: " + files[test_file_idx])
print(le.inverse_transform(clf.predict(tf_idf_vector[test_file_idx, :])))

# test
# read_pickle('../data/preprocessed/complaints', 'CA_FRE_01edFpSp4-OjCoEZwI46FA2.pkl')