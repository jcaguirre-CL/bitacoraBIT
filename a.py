#!/usr/bin/env python

#import smtplib
import os
import re
#import subprocess
#import time
#import datetime
#import time
#import fcntl
#import signal
import sys
import json
#import simplejson

progreso = 20

with open('/var/www/html/ingenieria/aplicaciones/progreso.json') as jsonFile:
	datos = json.load(jsonFile)
	datos['numbers'] = progreso
	print(datos)
	jsonFile.close()

with open('/var/www/html/ingenieria/aplicaciones/progreso.json', 'w') as jsonFile:
	jsonData = json.dumps(datos, indent=4, skipkeys=True, sort_keys=True)
	jsonFile.write(jsonData)
	jsonFile.close()
	


#json.dump(jsonData, open('/var/www/html/ingenieria/aplicaciones/progreso.json', 'wb'))

#with open("/var/www/html/ingenieria/aplicaciones/progreso.json","w") as jsonFile:
#	json.dump(jsonData, "/var/www/html/ingenieria/aplicaciones/progreso.json")
