FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN cat requirements.txt && pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./memcache-mon.py" ]