FROM ubuntu:20.04

ENV TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    software-properties-common \
    python3 \
    python3-pip \
    x11-xserver-utils \
    && add-apt-repository ppa:sumo/stable \
    && apt-get update \
    && apt-get install -y sumo sumo-tools sumo-doc

ENV SUMO_HOME=/usr/share/sumo

RUN pip3 install traci

COPY src/ /usr/src/app
WORKDIR /usr/src/app

CMD ["python3", "your_script.py"]
