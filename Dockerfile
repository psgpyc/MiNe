FROM python:3.7-alpine
MAINTAINER paritosh666

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir minecore
WORKDIR minecore
COPY ./minecore /minecore

RUN adduser -D user
USER user
