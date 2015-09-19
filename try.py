#! /src/bin/env python
# encoding: utf-8
# Demostració d'obtenció de la llista de cursos en Moodle
import re
from bs4 import BeautifulSoup

curs_escollit = "TEST"
tema_escollit = "Tema de Test"

# Obtenció de la pàgina principal de Moodle
soup = BeautifulSoup(open("dump.html"))
for form in soup.find_all("form", attrs={"id":"mform1"}):
    for entrada in form.find_all("input"):
        if entrada.has_attr("name") and entrada.has_attr("id"):
            print entrada["id"], entrada["name"]
    for textarea in form.find_all("textarea"):
        if textarea.has_attr("name"):
            print textarea["id"], textarea["name"]
    for select in form.find_all("select"):
        if select.has_attr("name"):
            print select["id"], select["name"]

