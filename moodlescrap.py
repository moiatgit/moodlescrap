#! /src/bin/env python
# encoding: utf-8

# Utilities for Moodle Scraping

import mechanize
from bs4 import BeautifulSoup
import re
from curs import MoodleCourse

class MoodleScrapper:
    """ encapsulates a session with moodle """

    def __init__(self, url, username, password):
        self._connect(url, username, password)
        self.mycourses = None


    def _connect(self, url, username, password):
        """ connects to the url with user and password.
            Returns mechanize Browser on exit. """
        self.br = mechanize.Browser()
        self.br.set_handle_robots( False )
        self.br.addheaders = [{'User-agent', 'Firefox'} ]

        # visitant Moodle
        self.br.open(url)
        self.follow_link("Entra amb Google")

        # signant amb Google
        assert self.br.viewing_html()
        self.br.select_form(nr=0)
        self.submit_form({"Email":username, "Passwd":password})

        # tornada a Moodle
        assert self.br.viewing_html()

    def follow_link(self, text):
        """ tries to follow the first link with the text """
        for l in self.br.links():
            if l.text == text:
                self.request = self.br.click_link(l)
                self.update_response(self.br.follow_link(l))
                break
        else:
            print "ERROR: link '%s' not found"%text

    def update_response(self, response):
        """ updates response and contents """
        self.response = response
        self.contents = BeautifulSoup(self.response.read())

    def submit_form(self, pairs):
        """ sets values and submits current form """
        for k, v in pairs.iteritems():
            self.br.form[k] = v
        self.update_response(self.br.submit())


    def submit_form_by_id(self, pairs):
        """ same as submit_form() but considering id instead of name """
        self.fill_form_by_id(pairs)
        self.update_response(self.br.submit())

    def submit_exercise(self, exercise):
        """ submits an exercise """
        self.fill_form_by_id(exercise.data)
        self.update_response(self.br.submit())

    def fill_form_by_id(self, pairs):
        """ sets values on current form where pairs key correspond with form controls' id """
        for k, v in pairs.iteritems():
            if v == None:
                continue
            control = self.br.form.find_control(id=k)
            if control.type=="checkbox":
                control.items[0].selected = v
            else:
                control.value = v

    def get_my_courses_list(self):
        """ selects the page with my courses and returns the list of them (id, name) """
        if self.mycourses == None:
            self.follow_link("Els meus cursos")
            soup = self.contents
            self.mycourses = []
            for curs in soup.find_all("div", attrs={'class': re.compile("coursebox.*")}):
                courseid = curs["id"][len("course-"):]
                coursetitle = curs.div.h2.a.text.encode("utf-8")
                courseurl = curs.div.h2.a["href"]
                self.mycourses.append(MoodleCourse(courseid, coursetitle, courseurl))
        return self.mycourses

    def select_form_by_id(self, formid):
        """ selects a form by attribute id.
            Returns True if form was found, False otherwise """
        for form in self.br.forms():
            if form.attrs['id'] == formid:
                self.br.form = form
                return True
        else:
            return False

    def openurl(self, url):
        """ opens a new url """
        self.update_response(self.br.open(url))

    def jump_to_course(self, coursename):
        """ jumps to coursename
            It returns True if course found """
        XXX vas per aquí: la idea és que disposes de self.courses i pots trobar si ja es troba el
        curs carregat per simplement seguir l'enllaç.
        Caldrà carregar la llista de cursos en cas que sigui None.

        self.follow_link
        soup = self.contents
        enrolled = soup.find("div", attrs={"class":"courses frontpage-course-list-enrolled"})
        if enrolled == None:
            return False
        for curs in enrolled.find_all("div", attrs={'class': re.compile("coursebox.*")}):
            nomcurs = curs.div.h3.a.text
            if nomcurs == coursename:
                novaurl=curs.div.h3.a["href"]
                break
        else:
            print "No s'ha trobat el curs", coursename
            return False
        self.openurl(novaurl)
        return True

    def disconnect(self):
        # finalitzant la sessió
        for l in self.br.links():
            if l.text == "Sortida":
                break
        else:
            l = None
        request = self.br.click_link(l)
        self.update_response(self.br.follow_link(l))
        assert self.br.viewing_html()
