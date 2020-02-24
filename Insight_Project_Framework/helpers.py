"""Helper functions."""

import yaml
import pickle
import os
from joblib import dump, load
from datetime import datetime

def read_pickle(text_folder_path, file_name):
    """
    Read a pickled file from a directory.

    Parameters:
    text_folder_path (string): path to the directory where the file is located
    file_name (string): name of file to read.

    Returns:
    read_text (string): text read from the pickle file.
    """
    with open(os.path.join(text_folder_path, file_name), 'rb') as filehandle:
        # read the data as binary data stream
        read_text = pickle.load(filehandle)
    return read_text

def read_yaml(config_path):
    """Load config files."""
    with open(config_path) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data

def ensure_dir(directory):
    """Check if directory exists. If not, create."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_model(classifier, model_folder):
    """Trim the classifier of unnecessary training data, and save it locally as a joblib."""
    # remove model word
    model_name = "model_" + datetime.now().strftime("%m-%d-%y_%H:%M:%S") + ".joblib"
    model_path = os.path.join(model_folder, model_name)
    # remove training information
    del classifier.word_processor.corpus
    del classifier.tf_idf_vector
    del classifier.X_train
    del classifier.X_test
    del classifier.y_train
    del classifier.y_test
    dump(classifier, model_path)
    print("Model saved at " + model_folder + ".")

def load_model(model_path):
    """Loads the saved joblib model."""
    clf = load(model_path) 
    return clf