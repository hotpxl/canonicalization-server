FROM ubuntu:trusty
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt-get update --yes && \
    apt-get install --yes python python-dev python-pip && \
    apt-get dist-upgrade --yes
COPY . /canonicalization-server
RUN cd canonicalization-server; pip install -r requirements.txt

EXPOSE 8080
CMD ["/bin/bash"]
