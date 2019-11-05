[![Codacy Badge](https://api.codacy.com/project/badge/Grade/eb23e0851b5341ac933dddbb331940eb)](https://www.codacy.com/app/M0NsTeRRR/DNSUpdateOVH?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=M0NsTeRRR/DNSUpdateOVH&amp;utm_campaign=Badge_Grade)
[![Docker Automated build](https://img.shields.io/docker/cloud/automated/monsterrr/dnsupdateovh?style=flat-square)](https://hub.docker.com/r/monsterrr/dnsupdateovh)
[![Docker Build Status](https://img.shields.io/docker/cloud/build/monsterrr/dnsupdateovh?style=flat-square)](https://hub.docker.com/r/monsterrr/dnsupdateovh)

The goal of this project is to update your DNS entries on OVH using OVH API. Feel free to update it to your use case.

## Requirements
#### Classic
- Python >= 3.7
- Pip3

#### Docker
- Docker CE

## Install

### Classic
Install the requirements `pip install -r requirements.txt`

Fill config.json with your informations (delay : delay between each check of your public address IP (60 <= delay <= 3600), create an application : [here](https://api.ovh.com/createToken/index.cgi?GET=/domain/zone/*&PUT=/domain/zone/*&POST=/domain/zone/*) )

Start the script `python main.py`

### Docker

Fill environment variable

`docker run -d --restart=always -e "UPDATEDNS_DELAY=" -e "UPDATEDNS_DOMAIN=" -e "UPDATEDNS_SUBDOMAIN=" -e "UPDATEDNS_APP_KEY=" -e "UPDATEDNS_APP_SECRET=" -e "UPDATEDNS_APP_CONSUMER_KEY=" monsterrr/dnsupdateovh:latest`

# Licence

The code is under CeCILL license.

You can find all details here: https://cecill.info/licences/Licence_CeCILL_V2.1-en.html

# Credits

Copyright © Ludovic Ortega, 2019

Contributor(s):

-Ortega Ludovic - mastership@hotmail.fr
