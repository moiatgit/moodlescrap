#! /src/bin/env python
# encoding: utf-8
# Demostració d'obtenció de la llista de cursos en Moodle
import os, base64
import mechanize
import re
from bs4 import BeautifulSoup

from moodlescrap import MoodleScrapper

fitxer_config = ".config/moodlescrap.dat"
# Obtenció de les dades de connexió
def obte_params_conf():
    """ obté els paràmetres url, usuari i pasword del fitxer de configuració """
    url = username = pasword = None
    if os.path.exists(fitxer_config):
        f = open(fitxer_config)
        url=f.readline().strip()
        username=f.readline().strip()
        password=base64.b64decode(f.readline().strip())
        f.close()
    return url, username, password

# obtenció de les dades de connexió
url, username, password = obte_params_conf()
moodle = MoodleScrapper(url, username, password)
print moodle.br.title()

# Obtenció de la pàgina principal de Moodle
soup = BeautifulSoup(moodle.response.read())
#for curs in soup.find_all('h3', class_="coursename"):
# for curs in soup.find_all('div', class_=re.compile("coursebox .*")):
#     print "Curs:", curs.div.h3.a.text
#     print "\tUrl:", curs.div.h3.a["href"]


# Desconnexió
moodle.disconnect()
print "URL    : ", moodle.response.geturl()
# print "Body: ", response.read()
#print "headers: ", moodle.response.info()



