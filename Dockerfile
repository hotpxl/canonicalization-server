FROM ubuntu:trusty
RUN apt-get update \
    apt-get install --yes python python-dev python-pip \
    apt-get dist-upgrade --yes
COPY . /canonicalization-server
RUN cd canonicalization-server; pip install -r requirements.txt

EXPOSE 8080
CMD ["/bin/bash"]
