import pickle
import os
import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn import svm
# from sklearn import preprocessing
# from sklearn.manifold import TSNE

# import pandas as pd
# import numpy as np

# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import cross_val_score
import string
from nltk.tokenize import word_tokenize 
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('words')
nltk.download('wordnet')
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer 

# import matplotlib.pyplot as plt
# from matplotlib import rcParams
# from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

def read_pickle(text_folder_path, file_name):
    with open(os.path.join(text_folder_path, file_name), 'rb') as filehandle:
        # read the data as binary data stream
        read_text = pickle.load(filehandle)
    return read_text

class Word_processor():
    def __init__(self, language, num_pages, county_names, text_folder_path):
        self.language = language
        self.lexicon = set(nltk.corpus.words.words())
        self.stop_words = set(stopwords.words(self.language))
        self.text_folder_path = text_folder_path
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.corpus = []
        self.labels = []
        
        # project specific variables
        self.num_pages = num_pages
        self.county_names = county_names
        self.lexicon_add_words(self.county_names)

    # function to add words to the english word lexicon. Used to add county names
    def lexicon_add_words(word_list):
        for phrase in word_list:
            for word in phrase.split(' '):
                self.lexicon.add(word) 

    # https://www.science-emergence.com/Articles/How-to-remove-string-control-characters-n-t-r-in-python/
    # replace string control chars with a space
    def remove_string_control_chars(self, text):
        regex = re.compile(r'[\n\r\t]')
        cleaned = regex.sub(" ", text)
        return cleaned
    
    # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
    def remove_punctuation(self, text):
        return text.translate(str.maketrans('', '', string.punctuation))

    def remove_spaces(self, text):
        return re.sub(' +', ' ', text)

    # function to remove numbers from a list of strings
    def remove_numbers(self, text):
        return [word for word in text if not word.isnumeric()]

    def list2string(self, word_list):
        return ' '.join(word_list)

    def remove_stop_words(self, text, language):
        # stop_words = set(stopwords.words(language))
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w in self.stop_words]
        return filtered_sentence

    def stem(self, tokens):
        stemmed = [self.stemmer.stem(word) for word in tokens]
        return stemmed

    def lemmatize(self, tokens):
#         lemmatizer = WordNetLemmatizer() 
        lemmatized = [self.lemmatizer.lemmatize(word) for word in tokens]
        return lemmatized
    
    # function to remove:
    #  1. numbers
    #  2. combination of alphabets and numbers
    #  3. stop words.
    # all the functions combined for performance.
    # essentially:
    # isalpha, in words and not in stopwords.
    def loop_cleaning(self, text):
        # tokenize
        # stop_words = set(stopwords.words(self.language))
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w in self.stop_words and w in self.lexicon and w.isalpha()]
        return filtered_sentence# [word for word in text if not word.isnumeric() or not word.isalpha() ]


    def clean_text(self, text):
        # lower the text
        cleaned = text.lower()
        # remove punctuations
        cleaned = self.remove_punctuation(cleaned)

        # remove string control characters
        cleaned = self.remove_string_control_chars(cleaned)
        # remove spaces 
        cleaned = self.remove_spaces(cleaned)

        # do above stop words, numbers and english lexicon filtering
        cleaned = self.loop_cleaning(cleaned)

        # stemming
        # cleaned = stem(cleaned)
        # lemmatizing
        cleaned = self.lemmatize(cleaned)
        # convert back to string
        # cleaned = nltk.Text(cleaned)
        cleaned = self.list2string(cleaned) 

        return cleaned

    def load_single_file_and_clean(self, file_name):
        text = read_pickle(self.text_folder_path, file_name)    
        if len(text) > self.num_pages:
            text = text[:self.num_pages]
        # concatenate texts from different pages
        text = '\n'.join(text)
        cleaned_text = self.clean_text(text)
        return cleaned_text

    
    # function to add words to the english word lexicon. Used to add county names
    def lexicon_add_words(self, word_list):
        for phrase in word_list:
            for word in phrase.split(' '):
                self.lexicon.add(word)
        # return lexicon
    
    
    def load_data_and_clean(self):
        files = os.listdir(self.text_folder_path)
        for file_name in files:
            clean_text = self.load_single_file_and_clean(file_name)
            self.corpus.append(clean_text)
            self.labels.append(file_name.split('_')[1])

if __name__ == "__main__":
    language = 'english'
    num_pages = 2
    county_names = ['fresno', 'kern', 'los angeles', 'santa clara', 'san francisco', 'san mateo']

    text_folder_path = os.path.join(os.environ['data_dir'], 'preprocessed/complaints')

    wp = Word_processor(language, num_pages, county_names, text_folder_path)
    wp.load_data_and_clean()
    print(wp.corpus[0])
    print(len(wp.corpus))