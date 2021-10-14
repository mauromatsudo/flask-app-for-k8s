FROM python:3.7-slim

RUN apt-get clean \
    && apt-get -y update 
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY . .

#ENV MYSQL_DATABASE_PORT==3306
#ENV db_user_password=password
#ENV MYSQL_SERVICE_HOST=192.168.111.7
#ENV db_name=book

RUN pip install -r requirements.txt --src /usr/local/src 

EXPOSE 5000
CMD [ "python", "conf_init_db.py" ]

