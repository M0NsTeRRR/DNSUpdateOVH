FROM python:3.7-alpine

LABEL maintainer="Ludovic Ortega mastership@hotmail.fr"

# update package
RUN apk update

# copy program and requirements
COPY main.py requirements.txt /app/DNSUpdateOVH/

# install dependencies
RUN pip3 install -r /app/DNSUpdateOVH/requirements.txt

CMD ["python3", "/app/DNSUpdateOVH/main.py"]