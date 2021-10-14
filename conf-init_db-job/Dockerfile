FROM python:3.7-alpine
WORKDIR /app
COPY requirements.txt .
RUN apk add --no-cache --virtual .build-deps build-base gcc libffi-dev openssl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps \
    && apk add --no-cache libcrypto1.1 libssl1.1
COPY . .
ENV MYSQL_DATABASE_PORT=3306
ENV db_user_password=password
ENV MYSQL_SERVICE_HOST=192.168.111.14
ENV db_name=book
RUN pip install --no-index --find-links=/app/wheels -r requirements.txt
EXPOSE 5000
CMD [ "python", "conf_init_db.py" ]

