"""Classifier class loads data, process and train a model."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn import preprocessing
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from Word_processor import *

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

    # simple predict
    def simple_inference(self, encoded_labels):
        correct_preds = 0
        result_DF = pd.DataFrame(np.zeros((len(self.word_processor.corpus), len(self.keys))), columns = self.county_names)
        for i in range(len(self.word_processor.corpus)):
            doc = self.word_processor.corpus[i]
            for j in range(len(self.county_names)):
                county_name = self.county_names[j]
                if county_name in doc:
                    result_DF.loc[i, county_name] = 1

        for i in range(len(result_DF)):
            if np.sum(result_DF.loc[i]) == 1 and np.where(result_DF.loc[i] == 1)[0][0] == encoded_labels[i]:
                correct_preds += 1
        print("baseline accuracy: " + str(correct_preds/len(encoded_labels)))

    def train(self):
        self.clf.fit(self.X_train, self.y_train)
    
    def evaluate(self):
        print("Mean accuracy over 6 1-vs-all linear SVMs: " + str(c.clf.score(c.X_test, c.y_test)))

if __name__ == "__main__":

    # language = 'english'
    # num_pages = 2
    # county_names = ['fresno', 'kern', 'los angeles', 'santa clara', 'san francisco', 'san mateo']

    # text_folder_path = os.path.join(os.environ['data_dir'], 'preprocessed/complaints')
    # keys = ['FRE', 'KC', 'LA', 'SCL', 'SFC', 'SM']
    # # 3000 counties in the states
    # # good balance between speed and performance
    # num_features = 10000
    
    # test_ratio = 0.2

    clf = svm.LinearSVC()

    c = Classifier(text_folder_path, num_pages, language, keys, county_names, num_features, clf, test_ratio)
    c.preprocess_fun()
    c.train()
    c.evaluate()