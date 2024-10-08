FROM python:3.12.4

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /usr/src/app

RUN pip install --upgrade pip
ADD ./requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app/