# Data downloading:
    run `python3 downloader.py`  
It will download the pdf files into data/raw/complaints.

# PDF file OCR:
    run `python3 OCR.py`  
It will process all the PDF files from data/raw/complaints and save the texts into data/preprocessed/complaints.

# Model training:
    run `python3 doc_type_classifier.py`  
It will read all the texts, generate a tf-idf matrix on all the words from the texts, and use the text as feature to train a multiclass SVM classifier, and output a sample prediction result. Train/test/CV split not yet implemented. tfidf kerword selection not yet implemented.