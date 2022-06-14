FROM python:3.11-rc-alpine
 
WORKDIR /app

COPY . /app/

COPY requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

