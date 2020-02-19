"""
Script to make inference by ids.

list of ids specified by ids in configs/config.xml.
"""

from helpers import *

if __name__ == "__main__":
    config_path = "../configs/config.yml"
    config = read_yaml(config_path)
    model_path = os.path.join(config["model_folder"], config["model_name"])

    c = load_model(model_path)
    result = c.predict_by_id(config["ids"])
    result_le_inverse = c.le.inverse_transform(result)
    print(result_le_inverse)
