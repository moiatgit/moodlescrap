#! /src/bin/env python
# encoding: utf-8
# Demostració de com afegir un exercici amb fitxer

print """XXX Aquesta prova no funciona
    El problema és que Moodle no ofereix un camp file en els formularis de tasca
    En canvi, hi ha un formulari amb l'etiqueta "Penja un fitxer" que podria ser seleccionat.
    Disposa d'un botó "Browse"
    Caldrà continuar investigant


    <div class="fp-navbar">
            <div class="filemanager-toolbar">
                <div class="fp-toolbar">
                    <div class="fp-btn-add">
                        <a role="button" title="Afegeix..." href="#">
                            <img src="http://agora.xtec.cat/insjoandaustria/moodle/theme/image.php/xtec2/core/1441294536/a/add_file" alt="Add file" />
                        </a>
                    </div>

"""

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


exercici = MoodleExercise("Exercici de prova avui", "Descripció de <b>prova</b>")
exercici.set_allowsubmissionsfromdate("20/9/2016 14:55")
exercici.add_file("try.py")
moodle.submit_exercise(exercici)



# desactiva l'edició
moodle.follow_link("Desactiva edició")

# Desconnexió
moodle.disconnect()
print "URL    : ", moodle.response.geturl()
# print "Body: ", response.read()
#print "headers: ", moodle.response.info()





