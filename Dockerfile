FROM python:3.10

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install wkhtmltopdf libcurl4-gnutls-dev librtmp-dev gcc libc-dev vim -y

COPY ./requirements.txt .

RUN pip install --upgrade setuptools
RUN pip install --upgrade pip
RUN python3 -m pip install --upgrade pip setuptools wheel

RUN pip install -v --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1
COPY . .