FROM ubuntu:latest

RUN apt-get update \
   && apt-get install -y apache2

RUN echo "ServerName localhost  " >> /etc/apache2/apache2.conf
RUN echo "$user     hard    nproc       20" >> /etc/security/limits.conf

WORKDIR /var/www/html
EXPOSE 80
CMD rm -f /var/run/apache2/apache2.pid && apachectl -D FOREGROUND
