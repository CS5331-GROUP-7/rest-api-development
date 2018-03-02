FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install -U pip
RUN pip install -U flask
RUN pip install -U flask-cors
RUN pip install -U pymongo
RUN pip install -U flask-sqlalchemy
RUN pip install -U flask-mongoengine

WORKDIR /usr/src/app

EXPOSE 8080

CMD ["python", "./service/app.py"]