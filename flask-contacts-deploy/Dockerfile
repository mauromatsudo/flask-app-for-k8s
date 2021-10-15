FROM debian:11-slim AS builder

WORKDIR /app

RUN apt update && apt install -y python3 python3-pip \
    python3-venv && python3 -m venv .venv && .venv/bin/pip3 \
    install --no-cache-dir -U pip setuptools

COPY requirements.txt .

RUN .venv/bin/pip install --no-cache-dir -r requirements.txt \
    && find /app/.venv -type f -a -name '*.pyc' -o -name '*.pyo'\
    -exec rm -rf '{}' \+

FROM debian:11-slim

WORKDIR /app

RUN apt update && apt install -y \
    apache2 libapache2-mod-wsgi-py3 python3 \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

COPY /flask-contacts.conf /etc/apache2/sites-available/flask-contacts.conf
COPY --from=builder /app /app
COPY . .

RUN a2ensite flask-contacts
RUN a2enmod headers

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 80
CMD /usr/sbin/apache2ctl -D FOREGROUND

