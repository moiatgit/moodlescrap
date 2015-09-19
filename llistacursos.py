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
enrolled = soup.find("div", attrs={"class":"courses frontpage-course-list-enrolled"})
for curs in enrolled.find_all("div", attrs={'class': re.compile("coursebox.*")}):
    print "Curs :", curs.div.h3.a.text
    print "\tUrl:", curs.div.h3.a["href"]
    print "\tId :", curs["data-courseid"]
    for teacher in curs.find("div", class_="content").find("ul", class_="teachers").find_all("li"):
        print "\tteacher:", teacher.text



# Desconnexió
moodle.disconnect()
print "URL    : ", moodle.response.geturl()
# print "Body: ", response.read()
#print "headers: ", moodle.response.info()



