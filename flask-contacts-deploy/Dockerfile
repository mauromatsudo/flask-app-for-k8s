FROM ubuntu:20.04 AS builder

WORKDIR /app

RUN apt update && apt install -y python3 python3-pip \
    python3-venv && python3 -m venv .venv && .venv/bin/pip3 \
    install --no-cache-dir -U pip setuptools

COPY requirements.txt .

RUN .venv/bin/pip install --no-cache-dir -r requirements.txt \
    && find /app/.venv -type f -a -name '*.pyc' -o -name '*.pyo'\
    -exec rm -rf '{}' \+

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    apache2 libapache2-mod-wsgi-py3 \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* \
    /var/log/dpkg.log \
    /var/lib/dpkg/status \
    /var/log/apt/history.log \
    /var/cache /var/log/apt \
    && a2dissite 000-default.conf \
    && rm -f /etc/apache2/sites-available/000-default.conf \
    rm -f /etc/apache2/sites-enabled/000-default.conf 


WORKDIR /app

COPY /flask-contacts.conf /etc/apache2/sites-available/flask-contacts.conf
COPY --from=builder /app /app
COPY . .

RUN chown -R 33:33 /var/log/apache2/ && a2ensite flask-contacts

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080
CMD /usr/sbin/apache2ctl -D FOREGROUND
