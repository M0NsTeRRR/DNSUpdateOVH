The goal of this project is to update your DNS entries on OVH using OVH API. Feel free to update it to your use case.

## Requirements

- Python >= 3.7
- Pip3

## Install

Install the requirements `pip install -r requirements.txt`

Fill config.json with your informations (delay : delay between each check of your public address IP (60 <= delay <= 3600), create an application : [here](https://api.ovh.com/createToken/index.cgi?GET=/domain/zone/*&PUT=/domain/zone/*&POST=/domain/zone/*) )

Start the script `python main.py`

# Licence

The code is under CeCILL license.

You can find all details here: http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html

# Credits

Copyright © Ludovic Ortega, 2019

Contributor(s):

-Ortega Ludovic - mastership@hotmail.fr