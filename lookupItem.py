#!/usr/bin/env python

import smtplib
import re
import datetime
import fcntl
import signal
import os
import shutil
import sys
import time
import logging
import subprocess
import json
import MySQLdb

#from sh import rsync
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import FileSystemEventHandler

def sacaOutput(nombreOutput):
    sacador = {
        "OUTPUT1": 1,
        "OUTPUT2": 2,
        "OUTPUT3": 3,
        "OUTPUT3": 4,
    }
    return sacador.get(nombreOutput, "valorDefault")

def modificarJson(nombre):
    with open('/var/www/html/ingenieria/aplicaciones/progreso.json') as jsonFile:
        datos = json.load(jsonFile)
        nombre1 = nombre.split("/")[5]
        datos['clip'] = nombre1.split("-")[0]
        datos['estado'] = 0
        datos['progreso'] = 0
        datos['inicio'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #print(datos)
        jsonFile.close()

    with open('/var/www/html/ingenieria/aplicaciones/progreso.json', 'w') as jsonFile:
        jsonData = json.dumps(datos, indent=4, skipkeys=True, sort_keys=True)
        jsonFile.write(jsonData)
        jsonFile.close()

def agregarRegistro(nombre, output1):
    db = MySQLdb.connect("localhost","root","ingeadmin","transcode")
    cur = db.cursor()
    nombre1 = nombre.split("/")[5]
    fecha1 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #cur.execute('''INSERT INTO trabajos (archivo, fechaInicio, progreso, estado, output) VALUES ( ?, ?, 0, 0, 1)''', ( nombre1, fecha1 ) )
    cur.execute('''INSERT INTO trabajos (archivo, fechaInicio, progreso, estado, output) VALUES (%s, %s, 0 , 0 , %s)''', (nombre1, fecha1, output1))
    db.commit()
    db.close()


class JcHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer
  
    def on_created(self, event):
        nombre = event.src_path
        logging.info(nombre)
        nombre = nombre.replace(" ", "")
        if not nombre == event.src_path:
            subprocess.call(['mv',event.src_path,nombre])
            logging.info('Eliminando espacios!!')
            logging.info(nombre)
        print nombre + "JcHandler"
        tmpNombre = "OUTPUT2"
        if 'mxf-WEB1200' in nombre:
            agregarRegistro(nombre.split(".mxf")[0]+'.mxf', sacaOutput(tmpNombre))
        if 'mp4-WEB1200' in nombre:
            agregarRegistro(nombre.split(".mp4")[0]+'.mp4', sacaOutput(tmpNombre))
        modificarJson(nombre)
        #os.system("/var/www/html/ingenieria/aplicaciones/sacaProgreso.py %s", nombre)
        proc = subprocess.Popen(["/var/www/html/ingenieria/aplicaciones/sacaProgreso.py", nombre])


if __name__ == "__main__":
    logfile = '/tmp/transcode/LOGs/porcentaje.log'
    print "Observando directorio!!!"
    logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(asctime)s :: %(levelname)s ::: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
    logging.info('Observando directorio!!!')
    path1 = "/tmp/transcode/LOGs/OUTPUT1"
    path2 = "/tmp/transcode/LOGs/OUTPUT2"
    path3 = "/tmp/transcode/LOGs/OUTPUT3"
    path4 = "/tmp/transcode/LOGs/OUTPUT4"
    observer1 = Observer()
    print observer1
    event_handler1 = JcHandler(observer1)
    observer1.schedule(event_handler1, path1, recursive=True)
    observer1.start()
    observer2 = Observer()
    print observer2
    event_handler2 = JcHandler(observer2)
    observer2.schedule(event_handler2, path2, recursive=True)
    observer2.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



