FROM continuumio/miniconda3
USER root

RUN apt-get update -y \
    gcc \
    poppler-utils \
    tesseract-ocr \
    libtesseract-dev \
    libcurl4-openssl-dev libssl-dev python-dev \
    curl \
    python3-pycurl \
&& apt-get autoremove -y \
&& apt-get clean \
&& apt-get autoclean \
&& rm -rf /var/lib/apt/lists/*

# COPY requirements.txt /
RUN mkdir data

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 -V
RUN python3 get-pip.py
RUN pip3 install update

# Download repo
RUN git clone https://github.com/shijiez777/Insight_Project.git
# move to Insight code repo and install dependencies
RUN cd Insight_Project/Insight_Project_Framework
RUN pip3 install -r requirements.txt

# Expose streamlit port
EXPOSE 8501
# Run streamlit module
RUN streamlit run streamlit_demo.py
CMD /bin/bash