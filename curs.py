#! /src/bin/env python
# encoding: utf-8

# Utility for encapsulating courses info in Moodle

class MoodleCourse:
    def __init__(self, courseid, coursename, courseurl):
        self.courseid = courseid
        self.coursename = coursename
        self.courseurl = courseurl
        self.themes = None

class MoodleTheme:
    def __init__(self, themeid, themename, themeurl):
        self.themeid = themeid
        self.themename = themename
        self.themeurl = themeurl
