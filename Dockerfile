FROM python:3.11-rc-alpine 
WORKDIR /app
COPY requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r ./requirements.txt


COPY . /app/


RUN python -m venv /py && \
   /py/bin/pip install --upgrade pip && \
   apk add --update alpine-sdk && \
   apk add --update --no-cache postgresql-client && \
   apk add --update --no-cache --virtual .tmp-build-deps \
      build-base gcc python3-dev postgresql-dev musl-dev libffi-dev openssl-dev cargo  && \
   /py/bin/pip install -r ./requirements.txt && \
   if [ $DEV = "true" ]; \
      then /py/bin/pip install -r ./requirements.txt ; \
   fi && \
   rm -rf /tmp && \
   apk del .tmp-build-deps && \
   adduser \
      --disabled-password \
      --no-create-home \
      django-user

