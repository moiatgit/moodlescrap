#! /src/bin/env python
# encoding: utf-8

# Utility for encapsulating courses info in Moodle

class MoodleCLI:
    """ encapsulates CLI utilities for Moodle """
    pass
# TODO: For now, just exercises (students, forums, etc. for the future)
#Define cli abstraction (data)
#    my courses, 
#        course, 
#            themes, 
#                exercises
#

#Define cli functions
#    mc   mycourses + themes
#    admc exercises
#    c    students
#    c    deliveries (download)
#    admc scores
#    admc forum entries

# design usage
#     moodlecli list mycourses
#     moodlecli list themes courseid
#     moodlecli list exercises themeid
#     moodlecli append exercise themeid exerciseparams
#     moodlecli update exercise exerciseid exerciseparams
#     moodlecli delete exercise exerciseid



class MoodleCourse:
    def __init__(self, courseid, coursename, courseurl):
        self.courseid = courseid
        self.coursename = coursename
        self.courseurl = courseurl
        self.themes = None
    def __str__(self):
        return str(self.__dict__)

class MoodleTheme:
    def __init__(self, themeid, themename, themeurl):
        self.themeid = themeid
        self.themename = themename
        self.themeurl = themeurl
    def __str__(self):
        return str(self.__dict__)

