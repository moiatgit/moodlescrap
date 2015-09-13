#! /src/bin/env python
# encoding: utf-8
import os, base64
import mechanize

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

# proves de connexió a Moodle
br = mechanize.Browser()
br.set_handle_robots( False )
br.addheaders = [{'User-agent', 'Firefox'} ]
br = mechanize.Browser()

# obtenció de les dades de connexió
url, username, password = obte_params_conf()

# visitant Moodle
br.open(url)
br.response().code
for l in br.links():
    if l.text == "Entra amb Google":
        break
else:
    l = None
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
print br.title()

# finalitzant la sessió
for l in br.links():
    if l.text == "Sortida":
        break
else:
    l = None
request = br.click_link(l)
response = br.follow_link(l)
print "URL    : ", response.geturl()
# print "Body: ", response.read()
print "headers: ", response.info()


