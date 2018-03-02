FROM ubuntu:latest

RUN sed -i 's/archive\.ubuntu\.com/ap-southeast-1\.ec2\.archive\.ubuntu\.com/g' /etc/apt/sources.list &&\
    apt update
ADD setup.sh requirements.txt /
RUN ls
RUN sh setup.sh
#RUN apt-get install -y python-pip
#RUN pip install -U pip
#RUN pip install -U flask
#RUN pip install -U flask-cors
#RUN pip install -U pymongo
#RUN pip install -U flask-sqlalchemy
#RUN pip install -U flask-mongoengine

WORKDIR /usr/src/app

EXPOSE 8080
# figure out how to change this based on ENV
CMD ["python", "./service/app.py"]
