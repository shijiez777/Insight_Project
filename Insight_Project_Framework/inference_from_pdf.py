from helpers import *
from OCR import threaded_OCR

if __name__ == "__main__":
    config_path = "../configs/config.yml"
    config = read_yaml(config_path)
    model_path = os.path.join(config["model_folder"], config["model_name"])
    c = load_model(model_path)

    # move to data directory
    # os.chdir(config['data_path'])
    pdf_folder_path = config["pdf_classification_path"]
    text_folder_path = config["processed_text_path"]

    threaded_OCR(pdf_folder_path, text_folder_path, config)

    # result = c.predict_by_id(config["ids"], config["num_pages"])
    # result_le_inverse = c.le.inverse_transform(result)
    # print(result_le_inverse)
