FROM python:3.9.6
ADD . /benfordParse
WORKDIR /benfordParse
RUN pip install -r requirements.txt