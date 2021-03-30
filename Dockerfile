FROM ubuntu:20.04
RUN apt update
RUN apt-get upgrade -y
RUN apt install -y python3 python3-pip python3-venv
RUN apt install vim -y

COPY poll_platform /home/poll_platform
RUN apt-get install -y virtualenv
WORKDIR /home/
RUN python3.8 -m venv ./venv
RUN ./venv/bin/activate
WORKDIR /home/poll_platform
RUN pip install -r requirements.txt

EXPOSE 8000