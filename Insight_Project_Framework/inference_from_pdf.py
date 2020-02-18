from helpers import *

if __name__ == "__main__":
    config_path = "../configs/config.yml"
    config = read_yaml(config_path)
    model_path = os.path.join(config["model_folder"], config["model_name"])
    c = load_model(model_path)


processed_text_path

    result = c.predict_by_id(config["ids"], config["num_pages"])
    result_le_inverse = c.le.inverse_transform(result)
    print(result_le_inverse)
