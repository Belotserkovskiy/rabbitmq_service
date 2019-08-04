FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./cfg ./cfg

CMD [ "python3", "./src/rabbitmq_service.py" ]