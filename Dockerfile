FROM ubuntu:20.04

LABEL Nathaniel Maki "njmaki[at]mtu.edu"

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

COPY ./requirements.txt /benfordParse/requirements.txt

WORKDIR /benfordParse

RUN pip install -r requirements.txt

COPY . /benfordParse

ENTRYPOINT [ “python” ]

CMD ["app.py"]
