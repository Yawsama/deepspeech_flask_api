FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip && \
    apt-get install -y sox

COPY . /spt_folder

WORKDIR /spt_folder

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]