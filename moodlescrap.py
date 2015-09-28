#! /src/bin/env python
# encoding: utf-8

# Utilities for Moodle Scraping

# TODO: a lot of robustesness is missing (e.g. not dealing with exceptions like config file not
# found)

import mechanize
from bs4 import BeautifulSoup
import re
from curs import MoodleCourse
from curs import MoodleTheme
import os, sys, base64
import mimetypes

class MoodleScrapper:
    """ encapsulates a session with moodle """

    _CONFIG_FILE = ".config/moodlescrap.dat"
    _DATA_FILE   = ".config/mycourses.pickle"


    def __init__(self):
        self._load_connection_params()
        self._connect()
        self.mycourses = None
        self.currentcourse = None

    def _load_connection_params(self):
        """ loads connection parameters from _CONFIG_FILE """
        self.url = self.username = self.pasword = None
        if os.path.exists(MoodleScrapper._CONFIG_FILE):
            f = open(MoodleScrapper._CONFIG_FILE)
            self.url=f.readline().strip()
            self.username=f.readline().strip()
            self.password=base64.b64decode(f.readline().strip())
            f.close()

    def _connect(self):
        """ connects to the url with user and password.
            Returns mechanize Browser on exit. """
        self.br = mechanize.Browser()
        self.br.set_handle_robots( False )
        self.br.addheaders = [{'User-agent', 'Firefox'} ]

        # visitant Moodle
        self.br.open(self.url)
        assert self.br.viewing_html()
        print "MoodleScrapper: at URL %s"%self.url
        self.follow_link("Entra amb Google")
        # signant amb Google
        assert self.br.viewing_html()
        print "MoodleScrapper: signing with Google"
        self.br.select_form(nr=0)
        self.submit_form({"Email": self.username, "Passwd": self.password})

        # tornada a Moodle
        assert self.br.viewing_html()
        print "MoodleScrapper: Signed"

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

    def submit_selected_form(self):
        """ submits selected form """
        self.update_response(self.br.submit())

    def submit_exercise(self, exercise):
        """ submits an exercise.
            It expects the corresponding form has been already selected """
        self.fill_form_by_id(exercise.data)
        response = self.br.submit()
        self.update_response(response)

    def submit_exercises_on_theme(self, courseid, themeid, exercises):
        """ submits an exercise after selecting the corresponding course and theme """
        formid = "section%s"%themeid
        self.jump_to_theme_by_id(courseid, themeid)
        # activate edition
        self.follow_link("Activa edició")

        for exercise in exercises:
            # selecciona el formulari del tema escollit
            if not self.select_form_by_id(formid):
                print "No s'ha trobat el formulari ", formid
                self.disconnect()
                sys.exit()
            # set adding a new task
            control = self.br.form.find_control("jump")
            control.items[19].selected = True
            self.submit_selected_form()
            self.br.select_form(nr=0)
            # actual submission
            self.submit_exercise(exercise)
            print "Submited exercise: %s"%exercise.data["id_name"]

        # deactivate edition
        self.follow_link("Desactiva edició")


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

    def get_my_courses(self):
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

    def get_themes_from_courseid(self, courseid):
        """ loads the themes from the course with id """
        self.get_my_courses()
        course = next( (c for c in self.mycourses if c.courseid == courseid), None)
        if course == None:
            print "ERROR: course id %s not found"%courseid
            return
        if course.themes == None:
            course.themes = []
            self.openurl(course.courseurl)
            for theme in self.contents.find_all("h3", attrs={"class":"section-title"}):
                themeid = theme.a["href"].split("=")[2]
                themename = theme.a.text
                themeurl = theme.a["href"]
                course.themes.append(MoodleTheme(themeid, themename, themeurl))
        return course.themes

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
        assert self.br.viewing_html()
        print "Now at URL %s"%url

    def jump_to_course_by_name(self, coursename):
        """ jumps to coursename
            It returns True if course found """
        self.get_my_courses()
        course = next( (c for c in self.mycourses if c.coursename == coursename), None)

        if course == None:
            return False

        self.openurl(course.courseurl)
        self.currentcourse = course
        return True

    def jump_to_course_by_id(self, courseid):
        """ jumps to course with id courseid
            It returns True if course found """
        self.get_my_courses()
        course = next( (c for c in self.mycourses if c.courseid == courseid), None)

        if course == None:
            return False

        self.openurl(course.courseurl)
        self.currentcourse = course
        return True

    def jump_to_theme_by_id(self, courseid, themeid):
        """ jumps to theme with id themeid
            It returns True if theme found """
        themes = self.get_themes_from_courseid(courseid)
        theme = next( (t for t in themes if t.themeid == themeid), None)
        if theme == None:
            return False
        self.openurl(theme.themeurl)
        self.currenttheme = theme
        return True

    def show_mycourses(self):
        """ shows the list of my courses """
        self.get_my_courses()
        print "My Courses list:"
        for course in self.mycourses:
            print "\tCourse [%s]:'%s' (%s)"%(course.courseid, course.coursename, course.courseurl)

    def show_themes_of_course(self, courseid=None):
        """ Shows the list of themes of current course """
        if courseid == None:
            if not self.currentcourse == None:
                courseid = self.currentcourse.courseid
        if courseid == None:
            print "No course selected yet"
            return
        themes = self.get_themes_from_courseid(courseid)
        for theme in themes:
            print "\tTheme [%s]: %s (%s)"%(theme.themeid, theme.themename, theme.themeurl)
        #self.jump_to_course_by_id(courseid)
        #print "List of themes for course %s"%self.currentcourse.coursename
        #for theme in self.contents.find_all("h3", attrs={"class":"section-title"}):
        #    print "\tsection_id:%s"%theme.a["href"].split("=")[2]
        #    

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
