FROM ubuntu:14.04
RUN apt-get update && apt-get install -y \
	openjdk-7-jre \
	nodejs \
	npm \
	curl
COPY /u3 /src
RUN cd /src; npm install
EXPOSE  3000
CMD ["nodejs", "/src/bin/www"]


