FROM python:3
USER root


ADD . /code
WORKDIR /code
RUN pip install --upgrade pip

RUN pip install -r requirements.txt
