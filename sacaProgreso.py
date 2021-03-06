#!/usr/bin/env python

import smtplib
import os
import re
import subprocess
import time
import datetime
import time
import fcntl
import signal
import sys
import json
import MySQLdb


#from configuration_vpn import config, cuentas
#from sys import platform as system_platform
from array import *

def calcularProgreso(line):
	try:
		#line = line.replace(" ","")
		print line
 		tiempo = line.split("=")
 		print tiempo
 		tiempo2 = tiempo[5].split()
 		print tiempo2
 		print tiempo[5]
 		print tiempo2[0]
 		tmp = [3600,60,1]
		duraTmp = sum([a*b for a,b in zip(tmp, map(int,tiempo2[0][:8].split(':')))])
		print duraTmp
 		return (duraTmp)
 		#return ((tiempo[14].split('<'))[1].split('>')[0])
 	except ValueError:
 		return ""

def agregarRegistro(nombre):
    db = MySQLdb.connect("localhost","root","ingeadmin","transcode")
    cur = db.cursor()
    nombre1 = nombre.split("/")[5]
    fecha1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #cur.execute('''INSERT INTO trabajos (archivo, fechaInicio, progreso, estado, output) VALUES ( ?, ?, 0, 0, 1)''', ( nombre1, fecha1 ) )
    cur.execute('''INSERT INTO trabajos (archivo, fechaInicio, progreso, estado, output) VALUES (%s, %s, 0 , 0 ,1)''', (nombre1, fecha1))
    db.commit()
    db.close()

def modificarJson(progreso, status):
	with open('/var/www/html/ingenieria/aplicaciones/progreso.json') as jsonFile:
		datos = json.load(jsonFile)
		datos['progreso'] = progreso
		datos['estado'] = status
		if progreso == 100:
			datos['estado'] = 1
		#print(datos)
		jsonFile.close()

	with open('/var/www/html/ingenieria/aplicaciones/progreso.json', 'w') as jsonFile:
		jsonData = json.dumps(datos, indent=4, skipkeys=True, sort_keys=True)
		jsonFile.write(jsonData)
		jsonFile.close()	

file = open(sys.argv[1])

total = 100
progreso = 0
duraInt = 0
log1 = 'time='
log2 = 'Duration'
log3 = 'overhead'
log4 = 'NULL'
log5 = 'Error'

num_lineas = sum(1 for line in file)
print num_lineas
file.seek(0)
ajuste_linea = []
ajuste = 0

for line in file:
	if log2 in line:
		line = line.rstrip()
		dura = (line.split())[1]
		print "aqui esta la duracion: " + dura[:8]
		#timestr = str(dura[8])
		dura2 = dura[:8]
		#print tmo2
		timestr = dura2
		#print timestr
		tmp = [3600,60,1]
		duraInt = sum([a*b for a,b in zip(tmp, map(int,timestr.split(':')))])
	ajuste_linea.append(ajuste)
	ajuste += len(line)

	if log4 in line:
		modificarJson(progreso,2)
		sys.exit(0)

	if log5 in line:
		modificarJson(progreso,2)
		sys.exit(0)


file.seek(ajuste_linea[num_lineas-1])
#print file.readline()

while progreso < 100:
	last = file.tell()
	linea = file.readline()
	print linea
	if not linea:
 		time.sleep(1)
 		file.seek(last)
	else:
		
		if log1 in linea:
		   	#print linea	
		   	#if progreso > duraInt:
		   	#		progreso = 100
		   	#print str(progreso) + "%"
		   	progreso = int((float(calcularProgreso(linea))*100)/duraInt)
		   	if progreso > 99:
		   		progreso = 100
			modificarJson(progreso,0)
		   
		if log3 in linea:
			progreso = 100
			#print str(progreso) + "%"
			modificarJson(progreso,1)

		if log4 in linea: 
		 	modificarJson(progreso,2)
		 	sys.exit(0)

		if log5 in linea: 
			modificarJson(progreso,2)
		 	sys.exit(0)

file.close()
