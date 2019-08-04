# ----------------------------------------------------------------------------
# Copyright © Ludovic Ortega, 2019
#
# Contributeur(s):
#     * Ortega Ludovic - mastership@hotmail.fr
#
# Ce logiciel, DNSUpdateOVH, est un programme informatique servant à mettre à jour des entrées DNS
# chez OVH
#
# Ce logiciel est régi par la licence CeCILL soumise au droit français et
# respectant les principes de diffusion des logiciels libres. Vous pouvez
# utiliser, modifier et/ou redistribuer ce programme sous les conditions
# de la licence CeCILL telle que diffusée par le CEA, le CNRS et l'INRIA
# sur le site "http://www.cecill.info".
#
# En contrepartie de l'accessibilité au code source et des droits de copie,
# de modification et de redistribution accordés par cette licence, il n'est
# offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,
# seule une responsabilité restreinte pèse sur l'auteur du programme,  le
# titulaire des droits patrimoniaux et les concédants successifs.
#
# A cet égard  l'attention de l'utilisateur est attirée sur les risques
# associés au chargement,  à l'utilisation,  à la modification et/ou au
# développement et à la reproduction du logiciel par l'utilisateur étant
# donné sa spécificité de logiciel libre, qui peut le rendre complexe à
# manipuler et qui le réserve donc à des développeurs et des professionnels
# avertis possédant  des  connaissances  informatiques approfondies.  Les
# utilisateurs sont donc invités à charger  et  tester  l'adéquation  du
# logiciel à leurs besoins dans des conditions permettant d'assurer la
# sécurité de leurs systèmes et ou de leurs données et, plus généralement,
# à l'utiliser et l'exploiter dans les mêmes conditions de sécurité.
#
# Le fait que vous puissiez accéder à cet en-tête signifie que vous avez
# pris connaissance de la licence CeCILL, et que vous en avez accepté les
# termes.
# ----------------------------------------------------------------------------

import logging
import json
from requests import get
from datetime import datetime
from time import sleep
from sys import exit

import ovh

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# endpoint to get this public address IP
urlIP = [
    'https://api.ipify.org',
    'https://ipinfo.io/ip',
    'https://ifconfig.me/'
]

# current IP address
currentIP = ''

# recordID of domain/subdomain to update
recordID = None

IPFound = False
recordIDFound = False

def getIP(url):
    """
    Get public address IP
    """
    r = get(url)
    if r.status_code == 200:
        return r.text.strip()
    else:
        raise Exception('Can\'t get IP from : {url}'.format(url))

# get configuration
try:
    with open('config.json') as json_data_file:
        config = json.load(json_data_file)
    if "delay" not in config or 60 <= config["delay"] >= 3600:
        raise Exception("config.json not filled properly")
    if "domain" not in config or not isinstance(config["domain"], str):
        raise Exception("config.json not filled properly")
    if "subDomain" not in config or not isinstance(config["subDomain"], str):
        raise Exception("config.json not filled properly")
    for OVHInfo in ["application_key", "application_secret", "consumer_key"]:
        if OVHInfo not in config["OVHClient"] or not isinstance(config["OVHClient"][OVHInfo], str):
            raise Exception("config.json not filled properly")
except Exception as e:
    logger.error("{error}".format(error=e))
    exit(1)


try:
    # Instanciate an OVH Client.
    # You can generate new credentials with full access to your account on
    # the token creation page
    client = ovh.Client(
        endpoint='ovh-eu',               # Endpoint of API OVH Europe (List of available endpoints)
        application_key=config["OVHClient"]["application_key"],    # Application Key
        application_secret=config["OVHClient"]["application_secret"], # Application Secret
        consumer_key=config["OVHClient"]["consumer_key"],       # Consumer Key
    )

    # Get record
    records = client.get('/domain/zone/' + config["domain"] + '/record', 
        fieldType='A', # Filter the value of fieldType property (like) (type: zone.NamedResolutionFieldTypeEnum)
        subDomain='', # Filter the value of subDomain property (like) (type: string)
    )

    if len(records) == 0:
        raise Exception("Found 0 record for {subDomain}.{domain}".format(subDomain=config["subDomain"], domain=config["domain"]))
    else:
        while not recordIDFound:
            for record in records:
                recordResult = client.get('/domain/zone/' + config["domain"] + '/record/' + str(record))
                if recordResult['zone'] == config["domain"] and recordResult['subDomain'] == config["subDomain"]:
                    recordID = recordResult['id']
                    currentIP = recordResult['target']
                    logger.info("Current IP : {currentIP}".format(currentIP=currentIP))
                    recordIDFound = True
        if recordID is None or currentIP == '':
            raise Exception("Found {nbRecords} records for {subDomain}{domain} but never found a record who match subdomain and domain".format(nbRecords=len(records), subDomain="" if config["subDomain"] == "" else config["subDomain"] + ".", domain=config["domain"]))    
except Exception as e:
    logger.error("{error}".format(error=e))
    exit(1)

while True:
    while not IPFound:
        for url in urlIP:
            try:
                resultIP = getIP(url)
                if currentIP != resultIP:
                    currentIP = resultIP
                    logger.info('New public IP address detected : {ip}'.format(ip=currentIP))
                    # Update record
                    client.put('/domain/zone/' + config["domain"] + '/record/' + str(recordID), 
                        target=currentIP, # Resource record target (type: string)
                    )
                    # Refresh record (required ?)
                    client.post('/domain/zone/' + config["domain"] + '/refresh')
                    logger.info('IP updated on {subDomain}{domain}'.format(subDomain="" if config["subDomain"] == "" else config["subDomain"] + ".", domain=config["domain"]))
                IPFound = True
            except Exception as e:
                logger.error("{error}".format(error=e))
        sleep(10)
    IPFound = False
    sleep(config["delay"])
