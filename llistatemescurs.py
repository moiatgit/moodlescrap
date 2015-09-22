#! /src/bin/env python
# encoding: utf-8
# Demostració d'obtenció de la llista de temes d'un curs en Moodle
import sys

from moodlescrap import MoodleScrapper
from exercise import MoodleExercise

curs_escollit = "TEST"
tema_escollit = "Tema de Test"

# obtenció de les dades de connexió
#url, username, password = obte_params_conf()
moodle = MoodleScrapper()

# Mostra la llista de cursos
moodle.show_mycourses()

# Obtenció de la pàgina amb el curs
moodle.jump_to_course_by_name(curs_escollit)

# Mostra temes del curs
moodle.show_themes_of_course()
#print "List of themes"
#soup = moodle.contents
#for tema in soup.find_all("h3", attrs={"class":"section-title"}):
#    print tema.a.text
#print soup
#for tema in soup.find_all("li", attrs={"aria-label":tema_escollit}):
#    print "\tTema [%s]:%s"%(tema[id], tema.h3.a.text)
#    #formid = "section%s"%tema["id"][len("section-")]
#
moodle.disconnect()
sys.exit()


# activa l'edició
moodle.follow_link("Activa edició")

# Troba tema per nom
soup = moodle.contents
for tema in soup.find_all("h3", attrs={"class":"section-title"}):
    if tema.h3.a.text == tema_escollit:
        formid = "section%s"%tema["id"][len("section-")]
        break
else:
    formid = None
    print "No s'ha trobat el tema ", tema_escollit
    moodle.disconnect()
    sys.exit()

# selecciona el formulari del tema escollit
if not moodle.select_form_by_id(formid):
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
moodle.submit_exercise(exercici)




# Desconnexió
moodle.disconnect()
print "URL    : ", moodle.response.geturl()
# print "Body: ", response.read()
#print "headers: ", moodle.response.info()




