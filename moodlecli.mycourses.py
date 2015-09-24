#! /src/bin/env python
# encoding: utf-8
# Demostració d'obtenció de la llista de temes d'un curs en Moodle
import sys
import argparse
from moodlescrap import MoodleScrapper

def compose_argparse():
    """ composes and returns an ArgumentParser """
    p = argparse.ArgumentParser(description = "Moodle Scrapper: list my courses", version="1.0")

    # Output options
    p.add_argument("-j", "--json", action="store_true",
                   help=u"Generate output in JSON format (csv otherwise)",
                   dest="jsonformat")

    return p

def exit_if_option_errors():
    """ it checks options and exists if inconsistent """
    pass        # no checks in this case

def get_options():
    """ returns option arguments  """
    p = compose_argparse()
    options = p.parse_args()
    return options

def run(options):
    """ executes the purpose of this program having options into account """
    moodle = MoodleScrapper()
    mycourses = moodle.get_my_courses()
    if len(mycourses) == 0:
        print "No courses found"
        return
    if options.jsonformat:
        for course in mycourses:
            print course
    else:
        print ",".join('"%s"'%c for c in mycourses[0].__dict__.keys())
        for course in mycourses:
            print ",".join('"%s"'%c for c in course.__dict__.values())

def main():
    options = get_options()
    run(options)
#
if __name__=="__main__":
    sys.exit(main())



