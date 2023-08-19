# Author: Haniye Kashgarani
# Affiliation: University of Wyoming
# Date: 2023-08-17T15:39:37+00:00
# Github: haniyeka

# Use an official Python 2.7 image
FROM python:2.7-slim-buster

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1

RUN pip install liac-arff pyyaml typing

COPY ./data_check_tool_python/ /usr/src/app/data_check_tool_python/

RUN chmod +x /usr/src/app/data_check_tool_python/src/*

RUN chmod +x /usr/src/app/data_check_tool_python/src/**/*

