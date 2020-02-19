FROM continuumio/miniconda3
USER root

RUN apt-get update -y
RUN apt-get install -y gcc

RUN apt-get install -y poppler-utils
RUN apt-get install -y tesseract-ocr
RUN apt-get install -y libtesseract-dev
RUN apt-get install -y libcurl4-openssl-dev libssl-dev python-dev

RUN apt-get install -y curl
RUN apt-get install -y python3-pycurl

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 -V
RUN python3 get-pip.py

RUN pip3 install update
COPY requirements.txt /
RUN mkdir data

RUN pip3 install -r requirements.txt

# Download repo
RUN git clone https://github.com/shijiez777/Insight_Project.git

CMD /bin/bash