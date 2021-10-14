FROM debian:11-slim

RUN apt update && \
    apt install -y apache2 \
    libapache2-mod-wsgi-py3 \
    #build-essential \
    python3 \
    #python-dev \
    python3-pip \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY /flask-contacts.conf /etc/apache2/sites-available/flask-contacts.conf
COPY . .

RUN pip3 install -r requirements.txt
RUN a2ensite flask-contacts
RUN a2enmod headers

ENV MYSQL_DATABASE_PORT==3306
ENV db_user_password=password
ENV MYSQL_DATABASE_PORT=3306
ENV MYSQL_SERVICE_HOST=192.168.111.7
ENV db_name=book

EXPOSE 80
CMD /usr/sbin/apache2ctl -D FOREGROUND

