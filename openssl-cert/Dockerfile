FROM debian:buster

RUN apt-get -y update
RUN apt-get -y install openssl

RUN mkdir -p /cert/

# Run script
COPY ./tools/script.sh /
RUN chmod +x /script.sh
ENTRYPOINT ["./script.sh"]