
FROM python:3.6.9

WORKDIR /usr/src/3papp

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -U pip

COPY ./requirements.txt /usr/src/3papp/requirements.txt
RUN apt-get -y update
RUN apt-get install -y libpq-dev
RUN apt-get install -y graphviz
RUN apt-get install -y graphviz-dev


RUN pip install -r requirements.txt

COPY . /usr/src/3papp/
WORKDIR /usr/src/3papp/src