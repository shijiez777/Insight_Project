import yaml

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
    with open(config_path) as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data