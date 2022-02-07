# FROM python:3.8.12-alpine3.15
#
# # set work directory
# WORKDIR /usr/src/app
#
# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
#
# # install dependencies
# #Dependancies for matplotlib, pandas, and numpy
# RUN apk add --no-cache --update \
#     python3 python3-dev gcc \
#     gfortran musl-dev g++ \
#     libffi-dev openssl-dev \
#     libxml2 libxml2-dev \
#     libxslt libxslt-dev \
#     jpeg-dev libjpeg make \
#     libjpeg-turbo-dev zlib-dev \
#     build-base wget libpng-dev openblas-dev \
#     py3-scipy
#
# RUN pip install --upgrade cython
# RUN pip install --upgrade pip
# RUN pip install --upgrade setuptools
#
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt
#
# # copy project
# COPY . .

# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/