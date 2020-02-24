# LeDoC
Legal document classification by counties.  

## Motivation
The client receives millions of legal documents every month and spends a lot of money parsing and classifying the documents. This project tackles the problem of classification of the documents by counties.

## Main idea

This package uses methods in computer vision and natural language processing to extract text from scanned PDFs, process the texts, and train a classifier to predict the county name using features extracted from the texts. More specifically, Google Tesseract is used to extract the text. After feature engineering, the data are fed into a one-vs-all SVM classifier.

## Presentation slides
Details about the motivation, methods and results can be found in my presentation [here](https://docs.google.com/presentation/d/1BxIq04CDL6nZnhcKT7H9yd9UgOVkiYbF6GAWi6DUfXA/edit?usp=sharing).

## Data
The data used are ~13k scanned PDF files. Links for downloading PDF files are stored in the metadata csv provided by the client, which is not included in the repo. 

## Environment setup
### Clone the repo
```
git clone https://github.com/shijiez777/Insight_Project.git
cd Insight_Project/Insight_Project_Framework/
```

### Build the docker image
The Environment can be set up using the included `Dockerfile` inside `Insight_Project_Framework` using command:
```
docker build --tag=ledoc .
```

### Prepare metadata needed for training

_This section is not necessary for inference._

To be able to train your own model, place the `metadata csv` inside the folder to be mounted to the docker container in `raw/metadata` directory.  

For example: `[PROJECT_DATA_DIRECOTRY]/raw/metadata/` should contain the metadata csv.  

For inference, the metadata file is not needed.

### Start the docker, mount the data directory and forward Streamlit port

```
docker run -v [PROJECT_DATA_DIRECOTRY]:/data -p 8501:8501 -it ledoc
```

For example, to mount the current directory while running the container:
```
docker run -v $(pwd):/data -p 8501:8501 -it ledoc
```
If you just want to test out inference, run:
```
docker run -p 8501:8501 -it ledoc
```


### Package configs
Please refer to and tune configs in `configs/config.yml` to suit your need. For example, increase `num_cores` to speed up OCR process.

## Inference
### Streamlit interface
From docker container, start streamlit service: 
```
streamlit run streamlit_demo.py
```

In your browser, go to `localhost:8501` and test out classification.

### Inference on all PDFs in a folder
1. In `configs/config.yml`: 
    - Specify folder containing PDF files to be classified: `prediction_pdf_path:`
    - specify folder for storing extracted text: `prediction_processed_text_path`
    - Specify folder for output: `prediction_output_path`

2. Inside `Insight_Project_Framework` run:
```
python3 inference_from_pdf.py 
```

### Infering documents by IDs:
1. Specify document IDs to be classified by modifying `id` in `configs/config.yml`

2. Inside `Insight_Project_Framework` run:
```
python3 inference_by_id.py 
```

## Training

### Download the PDF files from meetadata csv
1. Put the metadata csv inside `Insight_Project/data/raw/metadata`
2. Go the the `Insight_Project_Framework` and run the script to download the data using
```
python3 downloader.py
```
The data downloaded will be stored, by default, inside `[PROJECT_DATA_DIRECOTRY]/raw/complaints`

### Multithread text extraction using Tesseract OCR
Inside `Insight_Project_Framework` run:
```
python3 OCR.py
```
The extracted text will be stored by default, inside `[PROJECT_DATA_DIRECOTRY]/preprocessed/complaints` in pickle format.

### Text processing and training
To adjust county labels available the dataset for training, modify `county_names` and `keys` inside `configs/config.yml`.

Inside `Insight_Project_Framework` run:
```
python3 train.py
```
The trained model will be stored inside `models/`.

## Requisites
- poppler-utils
- tesseract-ocr
- libtesseract-dev

#### Dependencies
- pdf2image
- scikit-learn
- scipy
- numpy
- pytesseract
- nltk