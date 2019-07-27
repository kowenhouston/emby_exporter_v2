FROM python:alpine

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt

COPY emby_exporter/ /code/

EXPOSE 9123

ENTRYPOINT ["/usr/local/bin/python3", "/code/emby_exporter.py"]
