"""Word_processor class for loading and processing texts from pickle file."""

import re
import string
from nltk.tokenize import word_tokenize 
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('words', quiet=True)
nltk.download('wordnet', quiet=True)
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer 
from helpers import *

class Word_processor():
    """The class for processing and cleaning raw text.

    Attributes:
        num_pages (int): # number of pages/(elements in list) to parse. The text extracted
        Using OCR is structured as a list of strings, each element containts text from one
        page. num_pages limit number of pages to read in.
    """

    def __init__(self, language, num_pages, county_names, text_folder_path):
        """Initialize variables needed for the class instance."""
        self.language = language # string specifying language of document
        self.lexicon = set(nltk.corpus.words.words())
        self.stop_words = set(stopwords.words(self.language))
        self.text_folder_path = text_folder_path # path to the folder where texts are stored
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.corpus = []
        self.labels = []
        # project specific variables
        self.num_pages = num_pages
        self.county_names = county_names
        self.lexicon_add_words(self.county_names)

    # https://www.science-emergence.com/Articles/How-to-remove-string-control-characters-n-t-r-in-python/
    def remove_string_control_chars(self, text):
        """Replace string control chars with a space."""
        regex = re.compile(r'[\n\r\t]')
        cleaned = regex.sub(" ", text)
        return cleaned

    # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
    def remove_punctuation(self, text):
        return text.translate(str.maketrans('', '', string.punctuation))

    def remove_spaces(self, text):
        return re.sub(' +', ' ', text)

    def remove_numbers(self, text):
        """Remove numbers from a list of strings."""
        return [word for word in text if not word.isnumeric()]

    def list2string(self, word_list):
        return ' '.join(word_list)

    def remove_stop_words(self, text, language):
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w in self.stop_words]
        return filtered_sentence

    def stem(self, tokens):
        stemmed = [self.stemmer.stem(word) for word in tokens]
        return stemmed

    def lemmatize(self, tokens):
        lemmatized = [self.lemmatizer.lemmatize(word) for word in tokens]
        return lemmatized

    def loop_cleaning(self, text):
        """
        Perform all processings that need to iterate through all theelements in text.
        
        The functions are wrapped together to limit number of loops.
        This function removes:
        1. non-alphabetical tokens(number and digit-alphabet combination)
        2. stop words.
        3. tokens not found from english vocabulary
        all the procedures are combined for performance reasons.
        """
        word_tokens = word_tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w in self.stop_words and w in self.lexicon and w.isalpha()]
        return filtered_sentence

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
        cleaned = self.list2string(cleaned) 
        return cleaned

    def clean_and_concatenate_text(self, text):
        """Clean the OCR extracted text, and concatenate contents from different pages into 1 single long text."""
        if len(text) > self.num_pages:
            text = text[:self.num_pages]
        # concatenate texts from different pages
        text = '\n'.join(text)
        cleaned_text = self.clean_text(text)
        return cleaned_text


    def lexicon_add_words(self, word_list):
        """
        Add words to the english word lexicon.

        Arguments:
        word_list (list): list of words/phrases to be added to the lexicon
        """
        for phrase in word_list:
            for word in phrase.split(' '):
                self.lexicon.add(word)

    def load_training_data_and_clean(self):
        """Load and clean texts from the folder and store extracted corpus and labels as class variables."""
        files = os.listdir(self.text_folder_path)
        for file_name in files:
            text = read_pickle(self.text_folder_path, file_name)
            clean_text = self.clean_and_concatenate_text(text)
            self.corpus.append(clean_text)
            self.labels.append(file_name.split('_')[1])
        
    def load_data_for_prediction(self, processed_data_folder):
        """Load and clean texts for prediction and return."""
        cleaned_data = []
        files = os.listdir(processed_data_folder)
        for file_name in files:
            text = read_pickle(processed_data_folder, file_name)
            clean_text = self.clean_and_concatenate_text(text)
            cleaned_data.append(clean_text)
        return cleaned_data, files

if __name__ == "__main__":
    config_path = "../configs/config.yml"
    config = read_yaml(config_path)

    wp = Word_processor(config["language"], config["num_pages"], config["county_names"], config["text_folder_path"])
    wp.load_training_data_and_clean()
    print(wp.corpus[0])
    print(len(wp.corpus))