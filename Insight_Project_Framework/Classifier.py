"""Classifier class loads data, process and train a model."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn import preprocessing
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from Word_processor import *
from downloader import download_file_by_id
from OCR import bytes2text


class Classifier():
    """The class for processing and cleaning raw text.

    Attributes:
        num_pages (int): # number of pages/(elements in list) to parse. The text extracted
        Using OCR is structured as a list of strings, each element containts text from one
        page. num_pages limit number of pages to read in.
    """

    def __init__(self, text_folder_path, num_pages, language, keys, county_names, num_features, clf, test_ratio):
        """Initialize variables for Classifier class."""
        self.text_folder_path = text_folder_path
        self.num_pages = num_pages # number of pages to process
        self.language = language
        self.keys = keys # county keywords
        self.county_names = county_names
        self.word_processor = Word_processor(language, num_pages, county_names, text_folder_path)
        self.num_features = num_features # dimension of features
        self.feature_vectorizer = TfidfVectorizer(max_features=self.num_features)
        self.le = preprocessing.LabelEncoder()
        self.clf = clf
        self.test_ratio = test_ratio

    def preprocess_fun(self):
        self.word_processor.lexicon_add_words(self.county_names)
        # load data and clean
        self.word_processor.load_data_and_clean()
        # convert string labels to numerical
        self.encoded_labels = self.le.fit_transform(self.word_processor.labels)
        self.tf_idf_vector = self.feature_vectorizer.fit_transform(self.word_processor.corpus)
        # train test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.tf_idf_vector.toarray(), self.encoded_labels, test_size=self.test_ratio, stratify=self.encoded_labels)
        print("Training data processed.")

    # simple predict
    def simple_inference(self):
        correct_preds = 0
        result_DF = pd.DataFrame(np.zeros((len(self.word_processor.corpus), len(self.keys))), columns = self.county_names)
        for i in range(len(self.word_processor.corpus)):
            doc = self.word_processor.corpus[i]
            for j in range(len(self.county_names)):
                county_name = self.county_names[j]
                if county_name in doc:
                    result_DF.loc[i, county_name] = 1

        for i in range(len(result_DF)):
            if np.sum(result_DF.loc[i]) == 1 and np.where(result_DF.loc[i] == 1)[0][0] == self.encoded_labels[i]:
                correct_preds += 1
        print("baseline accuracy: " + str(correct_preds/len(self.encoded_labels)))

    def train(self):
        self.clf.fit(self.X_train, self.y_train)
        print("Model trained.")
    
    def evaluate(self):
        print("Mean accuracy over 6 1-vs-all linear SVMs: " + str(c.clf.score(c.X_test, c.y_test)))

    def predict_by_id(self, ids, num_pages):
        texts = []
        for id in ids:
            content = download_file_by_id(id)
            text = bytes2text(content, num_pages)
            cleaned_text = self.word_processor.clean_and_concatenate_text(text)
            texts.append(cleaned_text)
        X_pred = self.feature_vectorizer.transform(texts)
        y_pred = self.clf.predict(X_pred)
        return y_pred

    # def predict_from_folder(self, pdf_folder, num_pages):
    #     texts = []
    #     for id in ids:
    #         content = download_file_by_id(id)
    #         text = bytes2text(content, num_pages)
    #         cleaned_text = self.word_processor.clean_and_concatenate_text(text)
    #         texts.append(cleaned_text)
    #     X_pred = self.feature_vectorizer.transform(texts)
    #     y_pred = self.clf.predict(X_pred)
    #     return y_pred

if __name__ == "__main__":

    config_path = "../configs/config.yml"
    config = read_yaml(config_path)

    clf = svm.LinearSVC()

    c = Classifier(config["text_folder_path"], config["num_pages"], config["language"], config["keys"], config["county_names"], config["num_features"], clf, config["test_ratio"])
    c.preprocess_fun()
    c.simple_inference()
    c.train()
    c.evaluate()
