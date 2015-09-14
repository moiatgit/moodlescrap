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
        br = mechanize.Browser()
        br.set_handle_robots( False )
        br.addheaders = [{'User-agent', 'Firefox'} ]
        br = mechanize.Browser()

        # visitant Moodle
        br.open(url)
        br.response().code
        for l in br.links():
            if l.text == "Entra amb Google":
                break
        else:
            return None
        request = br.click_link(l)
        response = br.follow_link(l)

        # signant amb Google
        assert br.viewing_html()
        br.select_form(nr=0)
        br.form["Email"]=username
        br.form["Passwd"]=password
        response = br.submit()

        # tornada a Moodle
        assert br.viewing_html()
        self.br = br
        self.response = response

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

