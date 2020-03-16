# -*- coding: utf-8 -*-

import os
import sys
import csv
import pandas as panda
import uuid
import argparse
import numpy as np

#pour resneigner le fichier csv source (-src)
parser = argparse.ArgumentParser(description='Process the csv file source with -src | -h for help')
parser.add_argument('-src', type=str, help="Where the csv source file is located")
source = parser.parse_args()

#detecte l'endroit depuis lequel le script est lancé
script_location = os.path.dirname(os.path.realpath(__file__))

try:
    #ouverture de seulement les colonnes qui seront utiles au programme
    data = panda.read_csv(source.src, usecols = ['shortname', 'vpn'], sep = ";") 
except:
    print "La source renseigné ne renvoie sur aucun fichier csv avec les colonnes: shortname, vpn"
    sys.exit()

try: 
    #ouvre les fichier source MobileConfig (avec les valeurs à remplacer) dans une string pour pouvoir les manipuler
    mobileConfig = open(script_location+'/VPN_2019.mobileconfig','r')
    mobileConfig = str(mobileConfig.read())
except:
    print "Fichiers mobileConfig pas trouvé"
    sys.exit()
    
def createmobileconfig(line, mobileConfig, destination):
    #remplace les valeurs avec celles données
    mobileConfig = mobileConfig.replace("__SHORTNAME__",line['shortname'])
    mobileConfig = mobileConfig.replace("__PASSWORD__",line['vpn'])
    #création d'un UUID deterministique à partir d'une string (toujours le meme pour le meme string) grace à la méthode uuid5
    uuidString = uuid.uuid5(uuid.NAMESPACE_OID, line['shortname'])
    uuidString = str(uuidString)
    mobileConfig = mobileConfig.replace("__UUID1__",uuidString)
    #uuid à partir de l'email pour le calendrier (ajout de __CAL au string de l'email) 
    uuidString = uuid.uuid5(uuid.NAMESPACE_OID, line['shortname'] + "__FINAL")
    uuidString = str(uuidString)
    mobileConfig = mobileConfig.replace("__UUID2__",uuidString)

    #création du nouveau fichier avec les valeurs remplacées
    with open(script_location + "/" + destination+"/"+line['shortname']+".mobileconfig","wb") as final:
        final.write(mobileConfig)
        final.close

for i, row in data.iterrows():
    createmobileconfig(row, mobileConfig, "vpn")