#! /src/bin/env python
# encoding: utf-8

# Utilities for Moodle Scraping

import mechanize

class MoodleScrapper:
    """ encapsulates a session with moodle """

    def __init__(self, url, username, password):
        self._connect(url, username, password)


    def _connect(self, url, username, password):
        """ connects to the url with user and password.
            Returns mechanize Browser on exit. """
        self.br = mechanize.Browser()
        self.br.set_handle_robots( False )
        self.br.addheaders = [{'User-agent', 'Firefox'} ]

        # visitant Moodle
        self.br.open(url)
        self.br.response().code
        self.follow_link("Entra amb Google")

        # signant amb Google
        assert self.br.viewing_html()
        self.br.select_form(nr=0)
        #self.br.form["Email"]=username
        #self.br.form["Passwd"]=password
        #self.response = self.br.submit()
        self.submit_form({"Email":username, "Passwd":password})

        # tornada a Moodle
        assert self.br.viewing_html()

    def follow_link(self, text):
        """ tries to follow the first link with the text """
        for l in self.br.links():
            if l.text == text:
                self.request = self.br.click_link(l)
                self.response = self.br.follow_link(l)
                break
        else:
            print "ERROR: link '%s' not found"%text

    def submit_form(self, pairs):
        """ sets values and submits current form """
        for k, v in pairs.iteritems():
            self.br.form[k] = v
        self.response = self.br.submit()

    def submit_form_by_id(self, pairs):
        """ same as submit_form() but considering id instead of name """
        print "XXX pairs:%s"%pairs
        for k, v in pairs.iteritems():
            control = self.br.form.find_control(id=k)
            print "XXX trobat control %s %s %s %s"%(control.name, control.id, control.type, control.value)
            if control.type=="checkbox":
                print "XXX\t select!"
                control.selected = k
            else:
                print "XXX\t non select but %s"%control.type
                control.value = v
            print "XXX \t deixat control %s %s %s"%(control.name, control.id, control.value)
        self.response = self.br.submit()


    def openurl(self, url):
        """ opens a new url """
        self.response = self.br.open(url)

    def disconnect(self):
        # finalitzant la sessió
        br = self.br
        for l in br.links():
            if l.text == "Sortida":
                break
        else:
            l = None
        request = br.click_link(l)
        response = br.follow_link(l)
        assert br.viewing_html()
        self.br = br
        self.response = response

