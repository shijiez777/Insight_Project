import pickle

def read_pickle(text_folder_path, id):
    file_names = os.listdir(text_folder_path)
    with open(os.path.join(text_folder_path, file_names[id]), 'rb') as filehandle:
        # read the data as binary data stream
        read_text = pickle.load(filehandle)
    return read_text


