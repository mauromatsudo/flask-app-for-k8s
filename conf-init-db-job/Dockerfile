FROM python:3.7-alpine AS builder

WORKDIR /app

RUN apk add --no-cache build-base gcc libffi-dev openssl-dev \
    && python -m venv .venv \
    && .venv/bin/pip install --no-cache-dir -U pip setuptools

COPY requirements.txt .

RUN .venv/bin/pip install --no-cache-dir -r requirements.txt \
      && find /app/.venv -type f -a -name '*.pyc' -o -name '*.pyo'\
      -exec rm -rf '{}' \+

FROM python:3.7-alpine

WORKDIR /app

RUN apk add --no-cache libcrypto1.1 libssl1.1
ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app /app
COPY . .

EXPOSE 5000
CMD [ "python", "conf_init_db.py" ]

