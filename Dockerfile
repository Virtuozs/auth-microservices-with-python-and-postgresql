FROM python:3.11.1

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    && apt-get install sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app 

EXPOSE 5000

CMD ["python3", "server.py"]