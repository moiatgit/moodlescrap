#! /src/bin/env python
# encoding: utf-8
# Demostració de com afegir un exercici sense adjunts


import sys

from moodlescrap import MoodleScrapper
from exercise import MoodleExercise

cursid_escollit = "142"
temaid_escollit = "1"

moodle = MoodleScrapper()

moodle.jump_to_theme_by_id(cursid_escollit, temaid_escollit)


# activa l'edició
moodle.follow_link("Activa edició")

# Troba tema per nom
soup = moodle.contents
# print soup
# moodle.disconnect()
# sys.exit()

formid = "section%s"%temaid_escollit

# selecciona el formulari del tema escollit
if not moodle.select_form_by_id(formid):
    print "No s'ha trobat el formulari ", formid
    moodle.disconnect()
    sys.exit()

# set adding a new task
control = moodle.br.form.find_control("jump")
control.items[19].selected = True
moodle.submit_selected_form()

moodle.br.select_form(nr=0)

#print "="*100, "\n", moodle.contents, "="*100, "\n"


exercici = MoodleExercise("Exercici de prova avui", """
    <h1>Descripció de la prova</h1>
    <p>Aquesta és la descripció de <b>prova</b></p>
    <p>Tinc fins i tot un diagrama a mostrar! <img
                          src="http://moiatgit.github.io/apuntstecnics/images/poo003.img001.ascensor.png"></p>
                          """
                          )
exercici.set_allowsubmissionsfromdate("20/10/2016 14:55")
moodle.submit_exercise(exercici)



# desactiva l'edició
moodle.follow_link("Desactiva edició")

# Desconnexió
moodle.disconnect()
print "URL    : ", moodle.response.geturl()
# print "Body: ", response.read()
#print "headers: ", moodle.response.info()





