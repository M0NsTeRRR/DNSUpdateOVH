FROM python:3.7-alpine as build

LABEL maintainer="Ludovic Ortega mastership@hotmail.fr"

# update package
RUN apk update

# install git
RUN apk add git

# download DNSUpdateOVH project
RUN git clone https://github.com/M0NsTeRRR/DNSUpdateOVH

# remove config file
RUN rm DNSUpdateOVH/config.json

# copy file to /app/
RUN mkdir -p /app/DNSUpdateOVH/ && mv DNSUpdateOVH/* /app/DNSUpdateOVH/

# install dependencies
RUN pip3 install -r ./app/DNSUpdateOVH/requirements.txt

FROM python:3.7-alpine

# update package
RUN apk update

# copy DNSUpdateOVH
COPY --from=build /app/DNSUpdateOVH/ /app/DNSUpdateOVH/

# copy python library
COPY --from=build  /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/

CMD ["python3", "/app/DNSUpdateOVH/main.py"]