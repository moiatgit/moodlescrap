#! /src/bin/env python
# encoding: utf-8
# Demostració d'obtenció de la llista de temes d'un curs en Moodle
import sys, os, base64
import mechanize
import re
from bs4 import BeautifulSoup

from moodlescrap import MoodleScrapper
from exercise import MoodleExercise

curs_escollit = "TEST"
tema_escollit = "Tema de Test"

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
    nomcurs = curs.div.h3.a.text
    if nomcurs == curs_escollit:
        novaurl=curs.div.h3.a["href"]
        print "Nova URL:", novaurl
        break
else:
    print "No s'ha trobat el curs", curs_escollit
    moodle.disconnect()
    sys.exit()

moodle.openurl(novaurl)

# activa l'edició
moodle.follow_link("Activa edició")
soup = BeautifulSoup(moodle.response.read())
for tema in soup.find_all("li", attrs={"aria-label":tema_escollit}):
    if tema.h3.a.text == tema_escollit:
        formid = "section%s"%tema["id"][len("section-")]
        break
else:
    formid = None
    print "No s'ha trobat el tema ", tema_escollit
    moodle.disconnect()
    sys.exit()

# selecciona el formulari del tema escollit
for form in moodle.br.forms():
    if form.attrs['id'] == formid:
        moodle.br.form = form
        break
else:
    print "No s'ha trobat el formulari ", formid
    moodle.disconnect()
    sys.exit()

# troba l'identificador de l'afegiment d'exercici (es podria deduir)
form = tema.find("form", attrs={"id":formid})
select = form.find("select", attrs={"name":"jump"})
for option in select.find_all("option"):
    if option.text.strip() == "Tasca":
        value = option["value"]
        break
else:
    print "No s'ha trobat l'opció pel formulari de creació de tasca"
    moodle.disconnect()
    sys.exit()

moodle.submit_form({"jump":[value]})
moodle.br.select_form(nr=0)
exercici = MoodleExercise("Exercici de prova", "Descripció de <b>prova</b>")
exercici.set_allowsubmissionsfromdate("20/9/2016 14:55")
exercici.set_duedate("21/10/2017 15:50")
exercici.set_cutoffdate("19/11/2017 13:45")
moodle.submit_form_by_id(exercici.data)
#moodle.submit_form_by_id({"id_name":"exercici de prova", 
#                          "id_introeditor":"Descripció de <b>prova</b>",
#                          "id_allowsubmissionsfromdate_enabled":True,
#                          "id_allowsubmissionsfromdate_day":  ["20"],
#                          "id_allowsubmissionsfromdate_month":  ["10"],
#                          "id_allowsubmissionsfromdate_year":   ["2016"],
#                          "id_allowsubmissionsfromdate_hour":   ["23"],
#                          "id_allowsubmissionsfromdate_minute":   ["55"],
#                          "id_duedate_enabled":True,
#                          "id_duedate_day": ["21"],
#                          "id_duedate_month": ["10"],
#                          "id_duedate_year": ["2016"],
#                          "id_duedate_hour": ["23"],
#                          "id_duedate_minute": ["55"],
#                          "id_visible": ["0"], # Mostra:1
#                          })

#print "Body: ", moodle.response.read()



# Desconnexió
moodle.disconnect()
print "URL    : ", moodle.response.geturl()
# print "Body: ", response.read()
#print "headers: ", moodle.response.info()




