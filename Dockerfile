FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev net-tools nano vim default-jdk unzip\
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip 
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata  
  
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip -O corenlp.zip
RUN unzip corenlp.zip 
RUN rm corenlp.zip
RUN mv stanford-corenlp-full-2018-10-05 corenlp
RUN cp -r corenlp /usr/src/app/libs
ENV PYTHONPATH="/usr/src/app/src:/usr/src/app/src/programr${PYTHONPATH}"
EXPOSE 5000
RUN pip install --upgrade setuptools
RUN pip install spacy
RUN pip install -r requirements.txt
RUN python -m spacy download en
RUN mkdir bots/ryan/session_data
RUN chmod +x run.sh
