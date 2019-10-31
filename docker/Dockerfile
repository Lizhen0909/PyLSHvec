FROM python:3.6
MAINTAINER bochen "bochen0909@gmail.com"

USER root

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

RUN apt-get update  && apt-get install openjdk-11-jdk nodejs -y && apt-get clean && mkdir -p $JAVA_HOME/jre/lib/amd64 && ln -s $JAVA_HOME/lib/server $JAVA_HOME/jre/lib/amd64/server


RUN pip install --no-cache-dir Cython 
RUN pip install --no-cache-dir tqdm numpy pandas biopython jupyterlab jnius pylshvec

ADD jupyter_notebook /usr/bin/

CMD [ "/bin/bash" ]

