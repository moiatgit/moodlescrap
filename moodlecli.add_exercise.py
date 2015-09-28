#! /src/bin/env python
# encoding: utf-8
# This script adds new exercises to a theme in a moodle course
# User must provide for:
#   course id       : must be an existing course
#   theme id        : must be an existing theme
#   exercise list   : is a list of html files containing the definition of each exercise.
#                     Each file must contain a title that will be used as the exercise title

# TODO: an enhancement could be to accept .rst files. Furthermore, to accept a especific exercise included in
# a .rst file.
# TODO: In case there's an existing exercise with the same title, it should update instead of
# adding a new one

import sys, os
import argparse
from moodlescrap import MoodleScrapper
from exercise import MoodleExercise
from bs4 import BeautifulSoup
import datetime

def compose_argparse():
    """ composes and returns an ArgumentParser """
    p = argparse.ArgumentParser(description = "Moodle Scrapper: list my courses", version="1.0")

    # Input params
    p.add_argument('files', metavar='rstfiles', nargs='+', 
                   help="Exercise description file paths with .rst extension")
    p.add_argument("-c", "--courseid", action="store",
                   type=int,
                   required=True,
                   help=u"Moodle course id",
                   dest="courseid")
    p.add_argument("-t", "--themeid", action="store",
                   type=int,
                   required=True,
                   help=u"Moodle theme id",
                   dest="themeid")
    p.add_argument("-f", "--fromDate", action="store",
                   help=u"Date to start allowing submissions in the form dd/mm/yyyy hh:mm (defaults to today)",
                   dest="fromdate",
                   default= datetime.datetime.now().strftime("%d/%m/%Y %H:%%s")%(datetime.datetime.now().minute % 5 * 5))
    p.add_argument("-d", "--dueDate", action="store",
                   help=u"Due date in the form dd/mm/yyyy hh:mm",
                   dest="duedate")

    return p

def exit_if_option_errors(options):
    """ it checks options and exists if inconsistent """
    pass        # no checks in this case

def get_options():
    """ returns option arguments  """
    p = compose_argparse()
    options = p.parse_args()
    return options

def run(options):
    """ executes the purpose of this program having options into account """
    courseid = str(options.courseid)
    themeid = str(options.themeid)
    exercises = []
    for path in options.files:
        if not path.endswith(".html"):
            print "WARNING: unsuported format %s (ignored)"%path
            continue
        if not os.path.isfile(path):
            print "WARNING: file not found %s (ignored)"%path
            continue
        with open(path) as f:
            soup = BeautifulSoup(f.read())
            title = unicode(soup.title.text).strip().encode("utf-8")
            description = "\n".join(str(c).strip() for c in soup.body.div.contents if not c == None
                                    and len(str(c).strip())> 0
                                    and not c.name == "h1")
        exercise = MoodleExercise(title, description)
        if options.duedate:
            exercise.set_allowsubmissionsfromdate(options.fromdate)
            exercise.set_duedate(options.duedate)
        exercises.append(exercise)
    if len(exercises)>0:
        moodle = MoodleScrapper()
        moodle.submit_exercises_on_theme(courseid, themeid, exercises)
        moodle.disconnect()




def main():
    options = get_options()
    exit_if_option_errors(options)
    run(options)
    return
#
if __name__=="__main__":
    sys.exit(main())



