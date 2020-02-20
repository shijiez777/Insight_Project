# LeDoC
Legal document classification by counties.  
This package classifies complaint documents by county. 

## Main idea
This package uses methods in computer vision and natural language processing to extract text from PDFs, process the texts, and train a classifier to predict the county name using features extracted from the texts.

## Presentation slides
Details about the motivation, methods and results can be found in my presentation [here](https://docs.google.com/presentation/d/1BxIq04CDL6nZnhcKT7H9yd9UgOVkiYbF6GAWi6DUfXA/edit?usp=sharing).

# Environment setup
The Environment can be set up using the included `Dockerfile` inside `Insight_Project_Framework` using command:
```
docker build --tag=ledoc .
```

# To start the docker and mount the data directory:
```
docker run -v [DIRECTORY_WHERE_PDF_IS_STORED]:/data -it ledoc
```
For example, to mount the current directory while running the container:
```
docker run -v $(pwd):/data -it ledoc
```


## set up environment variables
In your bash file, add `Insight_Project` to the the git repo directory and `data_dir` where the data is to be stored:
```
    export Insight_Project=[PROJECT_DIRECTORY]
    export data_dir=[DATA_DIRECTORY]
```

## Download the data
1. Put the metadata csv inside `Insight_Project/data/raw/metadata`
2. Go the the `Insight_Project/Insight_Project_Framework` and run the script to download the data using
```
python3 downloader.py
```
The data downloaded will be stored inside `data_dir/raw/complaints`

# Preprocessing
## Multithread text extraction using Tesseract OCR
Inside `Insight_Project/Insight_Project_Framework` run:
```
python3 OCR.py
```
The extracted text will be stored inside `data_dir/preprocessed/complaints` in pickle format.

# Training
## Training the model
Inside `Insight_Project/Insight_Project_Framework` run:
```
python3 doc_type_classifier.py
```
The trained model will be stored inside `XXX/YYYY/ZZZ`.

# Evaluating

# Inference
## Infering locally:
Inside `Insight_Project/Insight_Project_Framework` run:
```
python3 infering.py -[DOCUMENT_ID]
```
### Specify paths related to inference on PDF files in configs/config.yml:
1. Specify folder containing PDF files to be infered: `prediction_pdf_path:`
2. specify folder for storing intermediate data: `prediction_processed_text_path`
3. Specify folder for output: `prediction_output_path`

### Run inference on pdfs:
```
python3 inference_from_pdf.py 
```

## Infering by document id:
### Specify parameters for inference by id in `configs/config.yml`: 
1. Specify ids of documents to be infered: `ids`
### Run inference by id:
```
python3 inference_by_id.py 
```
