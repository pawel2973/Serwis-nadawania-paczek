FROM jenkinsci/blueocean

USER root

WORKDIR .
COPY requirements.txt .

RUN apk add --no-cache --update \
    python3 \
    python-dev \
    build-base \
    && pip3 install --upgrade pip \
    && pip3 install coverage \
    && pip3 install requirements.txt \
    && rm -rf /var/cache/apk/* 

USER jenkins

#FROM jenkinsci/blueocean
#ENV PYTHONUNBUFFERED 1 
#WORKDIR .
#COPY requirements.txt .
