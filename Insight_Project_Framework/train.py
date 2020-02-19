"""Train and save the trained model."""

from Classifier import *

if __name__ == "__main__":
    config_path = "../configs/config.yml"
    config = read_yaml(config_path)
    clf = svm.LinearSVC()
    c = Classifier(config["text_folder_path"], config["num_pages"], config["language"], config["keys"], config["county_names"], config["num_features"], clf, config["test_ratio"])
    c.preprocess_fun()
    c.simple_inference()
    c.train()
    c.evaluate()
    save_model(c, config["model_folder"])