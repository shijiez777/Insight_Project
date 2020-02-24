FROM continuumio/miniconda3
USER root

RUN apt-get update \
&&  apt-get install  -y gcc \
    poppler-utils \
    tesseract-ocr \
    libtesseract-dev \
    libcurl4-openssl-dev libssl-dev python-dev \
    curl \
    python3-pycurl \
&& apt-get autoremove -y \
&& apt-get clean \
&& apt-get autoclean \
&& rm -rf /var/lib/apt/lists/* \
&& mkdir data

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
&& python3 get-pip.py \
&& pip3 install update

# Download repo and install dependencies
RUN git clone https://github.com/shijiez777/Insight_Project.git \
&& cd /Insight_Project/Insight_Project_Framework \
&& pip3 install -r requirements.txt

WORKDIR /Insight_Project/Insight_Project_Framework

# Expose streamlit port
EXPOSE 8501

CMD /bin/bash
