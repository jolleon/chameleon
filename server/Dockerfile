FROM python:3.6-alpine

MAINTAINER Jules Olleon <jolleon@gmail.com>

RUN pip install virtualenv

WORKDIR /app
COPY . /app
RUN virtualenv /env && /env/bin/pip install -r /app/requirements.txt

ENV CHAMELEON_PORT 5000
EXPOSE 5000
CMD ["/env/bin/python", "/app/chameleon.py"]
