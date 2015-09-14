#! /src/bin/env python
# encoding: utf-8
# Demostració d'obtenció de la llista de cursos en Moodle
import re
from bs4 import BeautifulSoup

# Obtenció de la pàgina principal de Moodle
soup = BeautifulSoup(open("llistacursos.html"))
enrolled = soup.find("div", attrs={"class":"courses frontpage-course-list-enrolled"})
for curs in enrolled.find_all("div", attrs={'class': re.compile("coursebox.*")}):
    print "Curs :", curs.div.h3.a.text
    print "\tUrl:", curs.div.h3.a["href"]
    print "\tId :", curs["data-courseid"]
    for teacher in curs.find("div", class_="content").find("ul", class_="teachers").find_all("li"):
        print "\tteacher:", teacher.text


