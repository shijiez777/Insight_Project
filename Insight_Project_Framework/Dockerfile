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

# Expose streamlit port
EXPOSE 8501

# Download repo
RUN git clone https://github.com/shijiez777/Insight_Project.git

# move to Insight code repo
RUN cd Insight_Project/Insight_Project_Framework
# Run streamlit module
RUN streamlit run streamlit_demo.py
CMD /bin/bash