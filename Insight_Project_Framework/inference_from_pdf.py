"""
Script to make inference to all the PDF files in a directory.

Directory of pdf files specified by prediction_pdf_path 
in configs/config.yml.

Directory to store OCRed text specified by prediction_processed_text_path
in configs/config.yml.

Directory to store prediction output specified by prediction_output_path
in configs/config.yml.
"""

from helpers import *
from OCR import threaded_OCR
import pandas as pd

if __name__ == "__main__":
    config_path = "../configs/config.yml"
    config = read_yaml(config_path)
    model_path = os.path.join(config["model_folder"], config["model_name"])
    c = load_model(model_path)

    # move to data directory
    pdf_folder_path = config["prediction_pdf_path"]
    text_folder_path = config["prediction_processed_text_path"]
    output_path = config["prediction_output_path"]
    ensure_dir(output_path)

    # extract text from PDF and save in text_folder_path
    threaded_OCR(pdf_folder_path, text_folder_path, config)

    text_files, result = c.predict_from_folder(text_folder_path)
    result_le_inverse = c.le.inverse_transform(result)

    results_with_filename = list(zip(text_files, result_le_inverse))
    for i in results_with_filename:
        print(i)

    pd.DataFrame(results_with_filename).to_csv(os.path.join(output_path, "output.csv"),index=False, header=False)

    # remove tmp files
    for file in text_files:
        os.remove(os.path.join(text_folder_path, file))