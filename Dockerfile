FROM ubuntu:trusty
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt-get update --yes && \
    apt-get install --yes python python-dev python-pip && \
    apt-get dist-upgrade --yes
COPY . /canonicalization-server
WORKDIR /canonicalization-server
RUN pip install -r requirements.txt
RUN python -m nltk.downloader -d /usr/share/nltk_data all

EXPOSE 80
CMD ["/canonicalization-server/start-server.sh"]
